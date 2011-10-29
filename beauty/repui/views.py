from collections import defaultdict
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from repui.api import dispatch
from repui.models import get_trenche_support
from beauty.data.treatments import TREATMENTS


#=---- - - - - - - - - - - - - - - - - - - - - - - - -
#
# API service.


def _json_boolean(n):
    return ("false", "true")[bool(n)]


def iapi(request):
    if __debug__:
        print request.POST
    res = dispatch(**request.POST)
    return HttpResponse(
        _json_boolean(res),
        mimetype="application/json",
        )


#=---- - - - - - - - - - - - - - - - - - - - - - - - -
#
# Main page of the iPad reps' UI.


def _prepare_trenche_data():
    d = defaultdict(list)
    for r in get_trenche_support():
        d[str(r['trenchelabel'])].append(str(r['treatmentname']))
    for default_trenche in "ABC":
        if default_trenche not in d:
            d[default_trenche] # force appearance of key.
    return [
        (k, sorted(d[k]))
        for k in sorted(d)
        ]


_t = [(k, TREATMENTS[k]) for k in sorted(TREATMENTS)]


def index(request):
    '''
    Rep UI page.
    '''
    return render_to_response(
        'index.html',
        dict(
            treatments=_t,
            trenches=_prepare_trenche_data(),
            ),
        context_instance=RequestContext(request),
        )


#=---- - - - - - - - - - - - - - - - - - - - - - - - -
#
# Search for available appointments.

from pprint import pprint as _P
from random import randint

def home(request):
    '''
    Search page.
    '''

    return render_to_response(
        'search.html',
        dict(),
        context_instance=RequestContext(request),
        )


def _fake_appt(n):
    return dict(
        spa = str(n) + "Barney's",
        rating = str(randint(0, 7)) + '/7',
        distance = 2.7 * (10 - n),
        distance_text = str(2.7 * (1 + n)) + ' miles',
        price = 1001.12 * n,
        )


def search(request):
##    if request.method != 'POST':
##        return redirect('home')

    _P(request.POST)

    return render_to_response(
        'results.html',
        dict(
            results = [
                _fake_appt(n)
                for n in range(7)
                ],
            ),
        context_instance=RequestContext(request),
        )






























