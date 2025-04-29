from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('basic_list/<int:pk>/', views.basic_list_view, name='basic_list'),
    path('manage_account/<int:pk>/', views.manage_account_view, name='manage_account'),
    path('delete_account/<int:pk>/', views.delete_account_view, name='delete_account'),
    path('change_password/<int:pk>/', views.change_password_view, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    path('better_menu/<int:pk>/', views.better_menu, name='better_menu'),
    path('add_menu/<int:pk>/', views.add_menu, name='add_menu'),
    path('view_detail/<int:pk>/', views.view_detail, name='view_detail'),
    path('delete_dish/<int:pk>/', views.delete_dish, name='delete_dish'),
    path('update_dish/<int:pk>/', views.update_dish, name='update_dish'),
]