from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from dotacje.models import Donation, Institution, Category
from .forms import RegistrationForm, LoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class GetData(View):
    def get(self, request):
        tab_type = request.GET.get('tab_type', 'Fundacje')
        print("Received tab_type:", tab_type)  # Debugging line

        if tab_type == 'Fundacje':
            data = list(Institution.objects.filter(type='1').values())
        elif tab_type == 'Organizacje pozarządowe':
            data = list(Institution.objects.filter(type='2').values())
        elif tab_type == 'Lokalne zbiórki':
            data = list(Institution.objects.filter(type='3').values())
        else:
            data = []

        print("Data count:", len(data))  # Debugging line
        return JsonResponse(data, safe=False)


class LandingPage(View):
    def get(self, request):
        donated_bags = Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags'] or 0
        number_of_institutions = Institution.objects.all().count()

        active_tab = request.GET.get('tab', 'Fundacja')

        context = {
            'bags': donated_bags,
            'no_institutions': number_of_institutions,
            'active_tab': active_tab,
            'Fundacja': Institution.objects.filter(type='1'),
            'Organizacja_pozarządowa': Institution.objects.filter(type='2'),
            'Lokalna_zbiórka': Institution.objects.filter(type='3'),
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
        form.instance.username = email
        form.instance.set_password(password)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main-page')


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'user_profile.html'

    def get(self, request):
        user = request.user
        context = {
            'user': user,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class FormView(View):
    template_name = 'form.html'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {
            'categories': categories,
            'instytucje': institutions
         }
        return render(request, self.template_name, context)
