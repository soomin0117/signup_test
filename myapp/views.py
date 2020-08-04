from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def main(request):
    return render(request, 'main.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    return render(request, 'login.html')

def signup(request):
    if request.method=='POST':
        user_form = CreateUserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid:
            user=user_form.save()
            profile = profile_form.save(commit=False)
            profile.user=user
            profile.image=profile_form.cleaned_data['image']
            profile.save()
            return redirect('/myapp/login/')           
        elif profile_form.is_valid() == False:
            me=profile_form.errors
            pro="Image upload ERROR"
            return render(request, 'hi.html', {'hi': me, 'pro':pro})
        elif user_form.is_valid() == False:
            pro="Input Data ERROR"
            me=user_form.errors
            return render(request, 'hi.html', {'hi': me, 'pro':pro})
        else:
            me="Something Wrong"
            return render(request, 'hi.html', {'hi': me}) 
    else:
        user_form = CreateUserForm()
        profile_form=ProfileForm()
        return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('/')
    else:
        return render(request, 'signup.html')