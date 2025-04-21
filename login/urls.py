from django.urls import path

from . import views

urlpatterns = [
    path("", views.log_user, name="log_user")
]