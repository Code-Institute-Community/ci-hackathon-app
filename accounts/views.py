from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import EditProfileForm


@login_required
def edit_profile(request):
    """ 
        If the request is POST and the form is valid, save the form and redirect to profile.
        Otherwise, display current user instance in EditProfileForm on edit_profile.html.
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

        else:
            messages.error(request, 'Invalid entry, please try again.')
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'accounts/edit_profile.html', {'form': form})
