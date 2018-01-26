import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from .models import Greeting

import sys
import peten_commander 
PETEN = peten_commander.Commander()

STARTING_TEXT="""
ברכה="שלום, עולם!"
להדפיס(ברכה)

### PETEN TRANSLATION COMMENTS ###
# ברכה = greeting
"""

def peten(request):
    if request.method == "POST":
         peten_text = request.POST["petenText"]
         #python_text = PETEN.process(peten_text)
         peten_filename = "./my_code.peten"
         f = open(peten_filename, "w")
         f.write(peten_text)
         f.close()
         python_filename = peten_commander.process_and_run_no_GUI(peten_filename, debug_mode=True, run_mode=False)
         python_text = open(python_filename).read()
         #logging.info(peten_text)
         #logging.info(python_text)
         context = {"python_text": python_text, "peten_text": peten_text}
         return render(request, 'peten.html', context)
    else:
        context = {"peten_text": STARTING_TEXT, "python_text": ""}
        return render(request, 'peten.html', context)

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

    
