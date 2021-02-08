from django.shortcuts import render, get_object_or_404
from hackathon.models import HackProject
from .forms import HackProjectSubmissionForm
"""Fuction that renders the submission page for the groups projects.
If the form submission is valid it takes the information and adds it to the DB"""


def submit(request):
    if request.method == 'POST':
        form_data = request.POST
        submission_form = HackProjectSubmissionForm(form_data)
        if submission_form.is_valid():
            submission = submission_form.save()
            return render(request, 'submissions/success.html')
    submission_form = HackProjectSubmissionForm()
    return render(request, 'submissions/submit.html',
                  {'submission_form': submission_form})
