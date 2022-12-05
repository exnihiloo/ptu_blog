from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('blog/<int:pk>', views.BlogDetail.as_view(), name='blogview'),
    path('add_blogpost/', views.CreateBlog.as_view(), name='add_blogpost'),
    path('blogpost/edit/<int:pk>', views.EditBlog.as_view(), name='edit_blogpost'),
]
