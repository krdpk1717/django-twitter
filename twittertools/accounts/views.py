from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import UpdateView 

from .forms import SignUpForm, UserProfileForm


class UpdateProfile(UpdateView):
    success_url = reverse_lazy('tweetfetch:index')
    template_name = 'account_update.html'
    form_class = SignUpForm
    form_profile = UserProfileForm

    # get current user object
    def get_object(self, queryset=None): 
        return self.request.user
    # def get(self, request):
    #     user = self.request.user
    #     form = self.form_class.objects.get(pk=user.pk)
    #     profile_form = self.form_profile.objects.get(user=user)
    #     context = {'form': form, 'profile_form': profile_form}
    #     return render(request, self.template_name, context)   

class SignUp(generic.CreateView):
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    form_class = SignUpForm
    form_profile = UserProfileForm

    #Display blank form
    def get(self, request):
        form = self.form_class(None)
        profile_form = self.form_profile()
        context = {'form': form, 'profile_form': profile_form}
        return render(request, self.template_name, context)

    #Process form data
    def post(self, request):
        form = self.form_class(request.POST)
        profile_form = self.form_profile(request.POST)
        context = {'form': form, 'profile_form': profile_form}
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)

            # Cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()

            # Returns User objects if credential are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('tweetfetch:index')
                    
        return render(request, self.template_name, context)
