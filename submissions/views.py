from django.shortcuts import render
from hackathon.models import HackProject

def submit(request):
    return render(request, 'submissions/submit.html')
