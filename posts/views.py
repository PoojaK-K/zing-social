import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post

# Temporary storage for OTPs (In a production app, use Redis or a Database)
temp_otp_storage = {}

def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'posts/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        # Stage 1: Initial Registration & OTP Sending
        if 'username' in request.POST and 'email' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return render(request, 'posts/register.html')

            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            temp_otp_storage[email] = {
                'otp': otp, 
                'username': username, 
                'password': password
            }
            
            # Send the OTP via your policynavinfo email
            send_mail(
                'Verify your Zing Social Account',
                f'Your verification code is: {otp}',
                'policynavinfo@gmail.com',
                [email],
                fail_silently=False,
            )
            return render(request, 'posts/verify_otp.html', {'email': email})

    return render(request, 'posts/register.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_otp = request.POST.get('otp')
        
        if email in temp_otp_storage and temp_otp_storage[email]['otp'] == user_otp:
            # OTP is correct! Create the actual user in the database
            user_data = temp_otp_storage[email]
            new_user = User.objects.create_user(
                username=user_data['username'], 
                email=email, 
                password=user_data['password']
            )
            new_user.save()
            del temp_otp_storage[email] # Clear storage
            messages.success(request, "Account verified! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'posts/verify_otp.html', {'email': email})

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'posts/login.html')

def messages_view(request):
    return render(request, 'posts/messages.html')