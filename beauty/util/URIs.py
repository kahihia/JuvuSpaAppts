try:
    from RDF import Uri
except ImportError:
    def Uri(thing):
        return thing


OUR_LAND = 'http://choicedocs.com/ref/'
OUR_LAND_URI = Uri(OUR_LAND)

PROVIDER = Uri(OUR_LAND + 'Provider')
TRENCHE = Uri(OUR_LAND + 'Trenche')
TREATMENT = Uri(OUR_LAND + 'Treatment')
PROCTYPE = Uri(OUR_LAND + 'ProcedureType')
CATEGORY = Uri(OUR_LAND + 'Category')
SUBCAT = Uri(OUR_LAND + 'SubCategory')
SUPPORTS = Uri(OUR_LAND + 'SupportsTreatment')
AVAIL = Uri(OUR_LAND + 'AvailabilitySlot')
DATE = Uri(OUR_LAND + 'Date')
WHERE = Uri(OUR_LAND + 'Location')
FROM_TIME = Uri(OUR_LAND + 'from_time')
TO_TIME = Uri(OUR_LAND + 'to_time')
EMPLOYS = Uri(OUR_LAND + 'Employs')

NAME = Uri('http://xmlns.com/foaf/0.1/name')
LABEL = Uri('http://www.w3.org/2000/01/rdf-schema#label')
TYPE = Uri('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')

##
##http://www.w3.org/2006/time#Interval
##http://www.w3.org/2006/time#xsdDateTime
##http://www.w3.org/2006/time#Instant
##


PREFIX = """\
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX cd: <http://choicedocs.com/ref/>
"""
