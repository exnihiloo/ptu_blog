from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name = "register"),
    path('edit_userprofile', views.update_profile, name = 'edit_userprofile'),
    path('change_password/', views.ChangePassword.as_view(), name="change_password"),
]
