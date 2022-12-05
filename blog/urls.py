from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('blog/<int:pk>', views.BlogDetail.as_view(), name='blogview'),
]
