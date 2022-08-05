from django.shortcuts import redirect, render, reverse
from django.contrib import messages

from competencies.forms import CompetencyForm, CompetencyDifficultyForm
from competencies.models import Competency


def list_competencies(request):
    competencies = Competency.objects.all()
    return render(request, 'list_competencies.html', {'competencies': competencies})


def create_competency_difficulty(request):
    if request.method == 'POST':
        form = CompetencyDifficultyForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            messages.success(request, "Competency Difficulty created successfully.")
            url = "%s?close_popup=true" % reverse('create_competency_difficulty')
            return redirect(url)
        else:
            print(form.errors)
            messages.error(request, form.errors)
            return redirect(reverse('create_competency_difficulty'))
            form = CompetencyDifficultyForm()
            return render(request, 'competency_difficulty_form.html', {'form': form})
    else:
        form = CompetencyDifficultyForm()
        return render(request, 'competency_difficulty_form.html', {'form': form})


def edit_competency_difficulty(request):
    if request.method == 'POST':
        pass
    else:
        form = CompetencyDifficultyForm()
        return render(request, 'competency_difficulty_form.html', {'form': form})


def create_competencies(request):
    if request.method == 'POST':
        pass
    else:
        form = CompetencyForm()
        return render(request, 'competency_form.html', {'form': form})


def edit_competencies(request):
    return render(request, 'competency_form.html')


def self_assess_competencies(request):
    return render(request, 'competencies_self_assessment.html')
