from __future__ import absolute_import

from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from forms import RegistrationForm, LoginForm

from braces import views


class HomePageView(generic.TemplateView):
    template_name = 'home.html'


class LoginView(
        views.AnonymousRequiredMixin,
        views.FormValidMessageMixin,
        generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'
    form_valid_message = "Your loggedin successfully "

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return form_invalid(form)


class SignUpView(
        # The AnonymousRequiredMixin prevents authenticated users from
        # accessing the view.
        views.AnonymousRequiredMixin,
        views.FormValidMessageMixin,
        generic.CreateView):
    form_class = RegistrationForm
    model = User
    form_valid_message = 'Thanks for signing up. Go ahead and login'
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        resp = super(SignUpView, self).form_valid(form)
        TalkList.objects.create(user=self.object, name='To Attend')
        return resp


class LogOutView(
        # The LoginRequiredMixin prevents this view from being accessed by
        # anonymous users.
        views.LoginRequiredMixin,
        views.MessageMixin,
        generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been logged out. Come back soon !")
        return super(LogOutView, self).get(request, *args, **kwargs)
        