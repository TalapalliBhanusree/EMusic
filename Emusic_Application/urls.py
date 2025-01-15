from django.contrib import admin
from django.urls import path, include
from app1 import views  # Import views from app1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('helpcenter/', views.helpcenter, name='helpcenter'),
    path('logout/', views.LogoutPage, name='logout'),
    path('subscribe/', views.subscribe, name='subscribe'),  
    path('payment/', views.payment, name='payment'),  
    path('payment_success/', views.payment_success, name='payment_success'),
    path('spotify/', views.spotify, name='spotify'),
    path('spotify/login/', views.spotify_login, name='spotify-login'),
    path('spotify/callback/', views.spotify_callback, name='spotify-callback'),
    path('home/', views.home_page, name='home'),
    path('search-results/', views.search_results, name='search_results'),
]