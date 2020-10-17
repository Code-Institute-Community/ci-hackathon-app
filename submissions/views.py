from django.shortcuts import render
from .models import Submission
from .forms import SubmissionForm

def submit(request):
    if request.method == 'POST':  # If the form has been submitted...
        form_data = request.POST
        submission_form = SubmissionForm(form_data)
        if submission_form.is_valid():
            submission = submission_form.save()
            return render(request, 'submissions/success.html')
    submission_form = SubmissionForm()

    context = {
        'submission_form': submission_form,
    }

    return render(request, 'submissions/submit.html', context)
