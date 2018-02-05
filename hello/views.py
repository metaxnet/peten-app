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

#import cmd
import subprocess

def peten(request):
    if request.method == "POST":
         logging.info(request.POST)
         logging.info(request.POST.keys())
         peten_text =  request.POST["petenText"]
         submit_mode = request.POST["submitMode"]
         #output_text = "OUTPUT"
         peten_filename = "./my_code.peten"
         f = open(peten_filename, "w")
         f.write(peten_text)
         f.close()
         python_filename = peten_commander.process_and_run_no_GUI(peten_filename, debug_mode=True, run_mode=False)
         python_text = open(python_filename).read()
         if submit_mode == "execute":
             process = subprocess.Popen(['python', python_filename], stdout=subprocess.PIPE)
             output_text, error_text = process.communicate()
             output_text = output_text.decode("utf8")
         else:
             output_text = "!"
         context = {"python_text": python_text, "peten_text": peten_text, "output_text": output_text, "submit_mode": submit_mode}        
         return render(request, 'peten.html', context)
    else:
        context = {"peten_text": STARTING_TEXT, "python_text": "", "output_text": "", "submit_mode": ""}
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

    
