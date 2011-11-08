from inspect import getargspec
from django.conf import settings
try:
    from RDF import (
        Storage,
        Model,
        Statement,
        Node,
        SPARQLQuery,
    )
except ImportError:
    from fake_rdf import (
        Storage,
        Model,
        Statement,
        Node,
        SPARQLQuery,
    )

from beauty.util.URIs import (
  NAME,
  PROVIDER,
  TRENCHE,
  TREATMENT,
  SUPPORTS,
  LABEL,
  TYPE,
  AVAIL,
  DATE,
  PREFIX,
  )


# One big ol' internal in-memory store. New on each restart.
M = Model(Storage(**settings.TRIPLE_STORES['default']))


def _query(sparql, **args):
  sparql = PREFIX + sparql
  return list(SPARQLQuery(str(sparql % args)).execute(M))


def plain_query(f):
  query = f.__doc__
  arg_names = getargspec(f).args
  def g(*args):
    return _query(query, **dict(zip(arg_names, args)))
  return g


@plain_query
def provider_named(name):
  """
  SELECT distinct ?a
  WHERE {
      ?a rdf:type cd:Provider .
      ?a foaf:name "%(name)s" .
  }
  """


def add_thing(name, label, kind):
  thing = Node()
  f = lambda p, o: Statement(thing, p, o)
  for s in (
    f(TYPE, kind),
    f(NAME, name),
    f(LABEL, label),
    ):
    M.add_statement(s)
  return thing


def add_provider(name, label):
  return add_thing(name, label, PROVIDER)


def add_treatment(name, label=None):
  if label is None:
    label, name = name, ''.join(name.split())
  return add_thing(name, label, TREATMENT)


def add_trenche(name):
  return add_thing(name, name, TRENCHE)


def add_treatment_to_trenche(treatment, trenche):
  T = get_treatment_from_label(treatment)
  treatment = T[0] if T else add_treatment(treatment)

  T = get_trenche_from_label(trenche)
  trenche = T[0] if T else add_trenche(trenche)

  s = Statement(trenche, SUPPORTS, treatment)
  if __debug__:
    print s
  M.add_statement(s)


def create_availability_with_trenche(trenche, day):
  T = get_trenche_from_label(trenche)
  if not T:
    if __debug__:
      print 'unknown trenche:', repr(trenche)
    return False # raise exception?
  trenche = T[0]
  avail = Node()
  M.add_statement(Statement(avail, TYPE, AVAIL))
  M.add_statement(Statement(avail, SUPPORTS, trenche))
  M.add_statement(Statement(avail, DATE, day))
  return avail


def get_treatment_from_label(label):
  return [
    t['treatment'] for t in _query("""
SELECT distinct ?treatment
WHERE {
    ?treatment rdf:type cd:Treatment .
    ?treatment rdfs:label "%(label)s" .
}
""",
  label=label,
  )]


def get_trenche_from_label(label):
  return [
    t['trenche'] for t in _query("""
SELECT distinct ?trenche
WHERE {
    ?trenche rdf:type cd:Trenche .
    ?trenche rdfs:label "%(label)s" .
}
""",
  label=label,
  )]


@plain_query
def get_trenche_support():
  """
  SELECT distinct ?trenchelabel ?treatmentname
  WHERE {
      ?trenche rdf:type cd:Trenche .
      ?trenche rdfs:label ?trenchelabel .
      ?treatment foaf:name ?treatmentname .
      ?trenche cd:SupportsTreatment ?treatment .
  }
  """


@plain_query
def get_avails_supporting_treatment(name):
  """
  SELECT distinct ?av
  WHERE {
      ?av cd:SupportsTreatment ?trenche .
      ?trenche cd:SupportsTreatment ?treatment .
      ?treatment foaf:name "%(name)s" .
  }
  """


@plain_query
def get_avails(treatment_name, date):
  """
  SELECT distinct ?av
  WHERE {
      ?av cd:SupportsTreatment ?trenche .
      ?trenche cd:SupportsTreatment ?treatment .
      ?treatment foaf:name "%(treatment_name)s" .
      ?av cd:Date "%(date)s" .
  }
  """


def prepare_trenche_data():
    '''
    Return a list of two-tuples containing "header" keys and lists of
    "content" strings suitable for building an Accordion thingy on the
    client side.
    '''
    d = defaultdict(list)
    for r in get_trenche_support():
        d[str(r['trenchelabel'])].append(str(r['treatmentname']))
    for default_trenche in "ABC":
        if default_trenche not in d:
            d[default_trenche] # force appearance of key.
    res = [
        (k, sorted(d[k]))
        for k in sorted(d)
        ]
    for k, v in res[:]:
        res.append((k + '_also', v))
    return res



##add_treatment("Acupuncture", "Acupuncture is Fun")
##add_treatment_to_trenche("Acupuncture is Fun", "A")
##create_availability_with_trenche("A")
##
##q = get_trenche_support()
##
##print
##print "%(tlabel)s supports %(ttname)s" % q[0]
##print




# Some simple debugging functions.

from collections import defaultdict

def subject():
  d = defaultdict(list)
  for s in M.as_stream():
    d[s.subject].append((s.predicate, s.object))
  for k in d:
    print k
    for p, o in d[k]:
      print '\t', p, '->', o
    print


def print_all():
  for i, s in enumerate(M.as_stream()):
    print "Statement %i:" % (i,), s




