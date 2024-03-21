from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
import africastalking

# Create your views here.
@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(form.cleaned_data)
            profile, created = Profile.objects.get_or_create(user=user)

          
            phone_number = form.cleaned_data.get('phone_number')
               
            if phone_number is not None:  # Check if phone_number is not None
                profile.phone_number = phone_number
                profile.save()
        # Send SMS only if phone_number is not None
                africastalking_username = 'kerry12'
                africastalking_api_key = 'b39c39b1548dec69f0bee899f7b8ff0ce38144276e860ad703e119fae90d7462'
        
                africastalking.initialize(africastalking_username, africastalking_api_key)
                sms = africastalking.SMS
                message = "Welcome to Our Neighbourhood App! We're excited to have you on board."
                response = sms.send(message, [profile.phone_number])
                print("SMS response:", response)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    return render(request, 'main/index.html')

@csrf_protect
@login_required(login_url='login')
def profile(request):
    return render(request, 'users/profile.html')


def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/editprofile.html', {'form': form})


def hoods(request):
    all_hoods = NeighbourHood.objects.all()
    all_hoods = all_hoods[::-1]
    params = {
        'all_hoods': all_hoods,
    }
    return render(request, 'main/all_hoods.html', params)


@login_required(login_url='login')
def create_hood(request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user
            hood.save()
            return redirect('hood')
    else:
        form = NeighbourHoodForm()
    return render(request, 'main/newhood.html', {'form': form})

@login_required(login_url='login')
def hood_details(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        businessform = BusinessForm(request.POST)
        if businessform.is_valid():
            biz_form = businessform.save(commit=False)
            biz_form.neighbourhood = hood
            biz_form.user = request.user.profile
            biz_form.save()
            return redirect('hood-details', hood.id)
    else:
        businessform = BusinessForm()
    params = {
        'hood': hood,
        'business': business,
        'businessform': businessform,
        'posts': posts
    }
    return render(request, 'main/hood-details.html', params)

@login_required(login_url='login')
def hood_members(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    members = Profile.objects.filter(neighbourhood=hood)
    return render(request, 'main/members.html', {'members': members})

@login_required(login_url='login')
def create_post(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('hood-details', hood.id)
    else:
        form = PostForm()
    return render(request, 'main/post.html', {'form': form})

@login_required(login_url='login')
def create_business(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    if request.method == 'POST':
        businessform = BusinessForm(request.POST)
        if businessform.is_valid():
            biz_form = businessform.save(commit=False)
            biz_form.neighbourhood = hood
            biz_form.user = request.user.profile
            biz_form.save()
            return redirect('hood-details', hood.id)
    else:
        businessform = BusinessForm()
    
    params = {
        'hood': hood,
        'business': business,
        'businessform': businessform
    }
    return render(request, 'main/business.html', params)


@login_required(login_url='login')
def join_hood(request, id):
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('hood')

@login_required(login_url='login')
def leave_hood(request, id):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hood')


def search_business(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'business-results': results,
            'message': message
        }
        return render(request, 'main/business-results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, "main/business-results.html")