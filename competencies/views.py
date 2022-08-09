from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render, reverse

from competencies.forms import (
    CompetencyForm, CompetencyDifficultyForm,
    CompetencyAssessmentForm, 
    CompetencyAssessmentRatingForm,
    RequiredModelFormSet)

from competencies.helpers import (
    get_or_create_competency_assessment,
    populate_competency_assessment_for_formset)

from competencies.models import (
    Competency, CompetencyDifficulty,
    CompetencyAssessment, CompetencyAssessmentRating)


def list_competencies(request):
    competencies = Competency.objects.order_by('display_name')
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
            messages.error(request, form.errors)
            return redirect(reverse('create_competency_difficulty'))
    else:
        form = CompetencyDifficultyForm()
        return render(request, 'competency_difficulty_form.html', {'form': form})


def edit_competency_difficulty(request, competency_difficulty_id):
    competency_difficulty = get_object_or_404(CompetencyDifficulty,
                                              id=competency_difficulty_id)
    if request.method == 'POST':
        form = CompetencyDifficultyForm(request.POST, instance=competency_difficulty)
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            messages.success(request, "Competency Difficulty edited successfully.")
            url = "%s?close_popup=true" % reverse('create_competency_difficulty')
            return redirect(url)
        else:
            messages.error(request, form.errors)
            return redirect(reverse('edit_competency_difficulty'))
    else:
        form = CompetencyDifficultyForm(instance=competency_difficulty)
        return render(request, 'competency_difficulty_form.html', {'form': form})


def create_competency(request):
    if request.method == 'POST':
        form = CompetencyForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            messages.success(request, "Competency created successfully.")
            return redirect(reverse('list_competencies'))
        else:
            messages.error(request, form.errors)
            return redirect(reverse('create_competency'))
    else:
        form = CompetencyForm()
        return render(request, 'competency_form.html', {'form': form})


def edit_competency(request, competency_id):
    competency = get_object_or_404(Competency,
                                   id=competency_id)
    if request.method == 'POST':
        form = CompetencyForm(request.POST, instance=competency)
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            f.save()
            messages.success(request, "Competency edited successfully.")
            return redirect(reverse('list_competencies'))
        else:
            messages.error(request, form.errors)
            return redirect(reverse('edit_competency'))
    else:
        form = CompetencyForm(instance=competency)
    return render(request, 'competency_form.html', {'form': form})


def self_assess_competencies(request):
    data = request.POST.copy()
    competencies = Competency.objects.filter(is_visible=True)
    try:
        competency_assessment = CompetencyAssessment.objects.get(
            user=request.user)
    except ObjectDoesNotExist:
        competency_assessment = None
    
    if request.method == 'POST':
        CompetencyAssessmentRatingFormSet = modelformset_factory(
            CompetencyAssessmentRating, fields=(
                'user_assessment', 'competency', 'rating'),
            form=CompetencyAssessmentRatingForm,
            formset=RequiredModelFormSet,
        )
        anything_filled_in = any(key.endswith('-rating')
                                 for key in data.keys())
        if not anything_filled_in:
            messages.error(request, 'Nothing selected.')
            return redirect(reverse('self_assess_competencies'))

        competency_assessment = get_or_create_competency_assessment(data)
        if not competency_assessment:
            messages.error(request, form.errors)
            return redirect(reverse('self_assess_competencies'))

        populate_competency_assessment_for_formset(competency_assessment, data)
        if competency_assessment:
            competency_assessments=competency_assessment.competencies.all()
        else:
            competency_assessments=CompetencyAssessmentRating.objects.none()
        formset = CompetencyAssessmentRatingFormSet(data,
            queryset=competency_assessments)

        if formset.is_valid():
            formset.save()
        else:
            messages.error(request, "Errors in the information")
            return redirect(reverse('self_assess_competencies'))
        return redirect(reverse('self_assess_competencies'))
    else:        
        initial=[]
        competency_assessments=[]
        if competency_assessment:
            assessment_competencies = competency_assessment.competencies
            if assessment_competencies.count() < competencies.count():
                competency_ids = [competency.id for competency in competencies]
                exclude_ids = [competency.id
                               for competency in assessment_competencies.all()
                               if competency.id not in competency_ids]
                competency_assessments = assessment_competencies.exclude(
                    id__in=exclude_ids)
                initial = [{'competency': competency}
                           for competency in competencies.all()
                            if competency.id not in [
                                c.id for c in competency_assessments]]
            else:
                competency_assessments = assessment_competencies.all()
            
        CompetencyAssessmentRatingFormSet = modelformset_factory(
            CompetencyAssessmentRating, fields=(
                'user_assessment', 'competency', 'rating'),
            form=CompetencyAssessmentRatingForm,
            formset=RequiredModelFormSet,
            extra=len(initial),
            )

        formset = CompetencyAssessmentRatingFormSet(
            queryset=competency_assessments,
            initial=initial,
        )

        if competency_assessment:
            form = CompetencyAssessmentForm(instance=competency_assessment)
        else:
            form = CompetencyAssessmentForm(initial={
                'user': request.user, 'is_visible': True})
        
        return render(request, 'competencies_self_assessment.html', {
            'form': form, 'competencies': competencies,
            'formset': formset,
})
