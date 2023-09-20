from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from dotacje.models import Donation, Institution
from .forms import RegistrationForm, LoginForm
from django.http import HttpResponseRedirect


class LandingPage(View):
    def get(self, request):
        donated_bags = Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags'] or 0
        number_of_institutions = Institution.objects.all().count()
        context = {
            'bags': donated_bags,
            'no_institutions': number_of_institutions
        }

        return render(request, "index.html", context)


class AddDonation(View):
    def get(self, request):
        return render(request, "add_donation.html")


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main-page')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            if User.objects.filter(username=email).exists():
                form.add_error(None, 'Niepoprawne hasło.')
                return render(self.request, self.template_name, {'form': form})
            else:
                form.add_error('email', 'Użytkownik o tym adresie email nie istnieje.')
                return HttpResponseRedirect(reverse_lazy('registration-page'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'register.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # Set the username to the email and hash the password
        form.instance.username = email
        form.instance.set_password(password)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main-page')
