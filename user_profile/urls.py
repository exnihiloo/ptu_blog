from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name = "register"),
    path('edit_userprofile', views.UserUpdate.as_view(), name = 'edit_userprofile'),
    path('change_password/', views.ChangePassword.as_view(template_name = 'registration/change_password.html' ), name="change_password")
]
