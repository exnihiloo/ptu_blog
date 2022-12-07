from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name = "register"),
    path('edit_userprofile', views.update_profile, name = 'edit_userprofile'),
    path('change_password/', views.ChangePassword.as_view(), name="change_password"),
    path('readlater/add_to_readlater/<int:id>', views.read_later, name = 'user_readlater'),
    path('readlater', views.readlaterview, name = 'readlater'),
    path('mydashboard/', views.mydashboard, name='mydashboard'),
    path('delete_profile/', views.deleteprofile, name = 'delete_profile'),
]
