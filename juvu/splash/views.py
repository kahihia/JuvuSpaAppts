# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from juvu.splash.models import proc_email


def splash(request):
    '''
    Splash page.
    '''
    return render_to_response(
        'index.html',
        context_instance=RequestContext(request),
        )


def record_email(request):
    '''
    Record emails from the splash page.
    '''
    if request.method == 'POST':
        email_addy = request.POST['record_email']
        proc_email(email_addy)
##        form = RecordEmailForm(request.POST)
##        if form.is_valid():
##            email_addy = form.cleaned_data['record_email']
    return redirect("/")

