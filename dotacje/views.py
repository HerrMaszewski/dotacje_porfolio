
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from dotacje.models import Donation, Institution, Category
from .forms import LoginForm, RegistrationForm, DonationForm


class GetData(View):
    def get(self, request):
        tab_type = request.GET.get('tab_type', 'Fundacje')
        print("Received tab_type:", tab_type)

        if tab_type == 'Fundacje':
            data = list(Institution.objects.filter(type='1').values())
        elif tab_type == 'Organizacje pozarządowe':
            data = list(Institution.objects.filter(type='2').values())
        elif tab_type == 'Lokalne zbiórki':
            data = list(Institution.objects.filter(type='3').values())
        else:
            data = []

        print("Data count:", len(data))
        return JsonResponse(data, safe=False)


class LandingPageView(View):
    def get(self, request):
        bags = 0
        institutions = []
        donations = Donation.objects.all()

        for donation in donations:
            bags += donation.quantity
            if donation.institution.name not in institutions:
                institutions.append(donation.institution.name)
        institutions = len(institutions)

        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)

        return render(request, 'index.html',
                      {'bags': bags, 'institutions': institutions,
                       'foundations': foundations, 'organizations': organizations,
                       'local_collections': local_collections})


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        form = DonationForm()
        return render(request, 'form.html',
                      {'categories': categories, 'institutions': institutions, 'form': form})

    def post(self, request):
        form = DonationForm(request.POST)
        categories = request.POST['categories']
        institution = request.POST['institution']
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']
            phone_number = form.cleaned_data['phone_number']
            pick_up_date = form.cleaned_data['pick_up_date']
            pick_up_time = form.cleaned_data['pick_up_time']
            pick_up_comment = form.cleaned_data['pick_up_comment']
            user = request.user.id
            donation = Donation.objects.create(quantity=quantity, institution_id=institution, address=address,
                                               city=city, zip_code=zip_code, phone_number=phone_number,
                                               pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                               pick_up_comment=pick_up_comment, user_id=user)
            donation.categories.add(categories)
            return render(request, 'form-confirmation.html')
        else:
            categories = Category.objects.all()
            institutions = Institution.objects.all()
            return render(request, 'form.html',
                          {'categories': categories, 'institutions': institutions, 'form': form})


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
