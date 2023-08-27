from .models import User
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib import messages

# Create your views here.
def registerPage(request):
    if request.method =='POST':
        email=request.POST['email']
        password=request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.info(request,'User already exists')
            return redirect('loginPage')
        else:
            # messages.error(request,'Invalid user type ! Try again.')
            user=User.objects.create_user(email=email,password=password,user_type=1)
            user.save()
            #return statement required
            return redirect('loginPage')
    else:
        return render(request,'register.html')



def loginPage(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        request.session['customer']=user.id
        if user is not None:
            auth.login(request,user)
        #return statement required
        return redirect('homePage')
    else:
        return render(request,'login.html')


def logout(request):
    request.session.clear()
    auth.logout(request)
    return redirect('/')