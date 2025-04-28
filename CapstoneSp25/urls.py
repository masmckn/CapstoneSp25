"""
URL configuration for CapstoneSp25 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from login.views import logout_view, create_account, insurance_info
from dashboard.views import user_profile, change_pass, payment, delete_account, insurance_details

urlpatterns = [
    path('login/', include('login.urls')),
    path('', include('login.urls')),
    path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', include('dashboard.urls')),
    path('register/', create_account, name='create_account'),
    path('profile/', user_profile, name='profile'),
    path('profile/update/', change_pass, name='change_pass'),
    path('payment/', payment, name='payment'),
    path('insuranceinfo/', insurance_info, name='insurance_info'),
    path('deleteaccount/', delete_account, name='delete_account'),
    path('insurancedetails/', insurance_details, name='insurance_details'),
]
