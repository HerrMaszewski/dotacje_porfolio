"""
URL configuration for dotacje_portfoliolab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dotacje.views import LandingPage, AddDonation, LoginView, RegistrationView, LogoutView, UserProfileView, FormView, GetData

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', LandingPage.as_view(), name="main-page"),
    path('add-donation/', AddDonation.as_view(), name="add-donation"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegistrationView.as_view(), name="registration-page"),
    path('user-profile/', UserProfileView.as_view(), name="user-profile"),
    path('form/', FormView.as_view(), name="form"),
    path('get_data/', GetData.as_view(), name='get_data'),
# path('user-profile-settings/', UpdateUserProfile.as_view(), name="profile-settings"),
]
