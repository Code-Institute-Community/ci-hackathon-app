from django.shortcuts import render
from .models import Submission
from .forms import SubmissionForm

def submit(request):
    if request.method == 'POST':  # If the form has been submitted...
        submission_form = SubmissionForm(request.POST)
    submission_form = SubmissionForm()

    context = {
        'submission_form': submission_form,
    }

    return render(request, 'submissions/submit.html', context)
