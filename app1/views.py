from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings


@login_required(login_url='login')
def Dashboard(request):
    return render(request, "dashboard.html")

def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("Your password and confirm password are not matched!")
        else:
            my_user = User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username or Password is incorrect!")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def about(request):
    return render(request, "about.html")

def helpcenter(request):
    return render(request, "helpcenter.html")
    
def subscribe(request):
    return render(request, 'subscribe.html') 

def payment(request):
    if request.method == "GET":
       
        plan = request.GET.get("plan", "Free")
        
        pricing = {
            "Free": 0,
            "Premium": 9.99,
            "Family": 14.99,
        }
        
        amount = pricing.get(plan, 0)  

        return render(request, "payment.html", {"plan": plan, "amount": amount})

    elif request.method == "POST":
        card_number = request.POST.get("cardNumber")
        expiry_date = request.POST.get("expiryDate")
        cvv = request.POST.get("cvv")
        plan = request.POST.get("plan")

        if card_number and expiry_date and cvv:
            return render(request, "payment_success.html", {"plan": plan})
        else:
            return HttpResponse("Payment failed. Invalid details.", status=400)
        
def payment_success(request):
    return render(request, "payment_success.html")

def spotify(request):
    return render(request, 'spotify.html')


SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1/"

def spotify_login(request):
    scopes = "user-read-private user-read-email user-library-read playlist-read-private"
    auth_url = f"{SPOTIFY_AUTH_URL}?client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={settings.SPOTIFY_REDIRECT_URI}&scope={scopes}"
    return redirect(auth_url)


def spotify_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Authorization code not found.'}, status=400)

    
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
    token_data = response.json()

    if 'access_token' in token_data:
        access_token = token_data['access_token']
        headers = {"Authorization": f"Bearer {access_token}"}
        user_profile = requests.get(SPOTIFY_API_BASE_URL + "me", headers=headers).json()
        
        spotify_web_player_url = "https://open.spotify.com/"
        return redirect(spotify_web_player_url)
    else:
        return JsonResponse({'error': 'Failed to fetch access token.'}, status=400)

def home_page(request):
    return render(request, 'home.html')

def search_results(request):
    return render(request,'search_results.html')

