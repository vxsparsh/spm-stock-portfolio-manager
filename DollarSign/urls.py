from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('portfolio/', portfolio, name='portfolio'),
    path('delete_stock/<str:stock_symbol>/', views.delete_stock, name='delete_stock'),
    path('register/', register, name='register'),  # for the registration page
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('store_data/', views.store_data_in_session, name='store_data'),
    path('retrieve_data/', views.retrieve_data_from_session, name='retrieve_data'),
    # ...
]


