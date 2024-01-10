from django.shortcuts import render,redirect
from django.views.generic import View
from reminder.forms import UserForm,SignInForm,TodoForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from reminder.models import Todos
from django.utils.decorators import method_decorator
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"please signin to continue session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def owner_permission_required(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        if Todos.objects.get(id=id).user != request.user:
            messages.error(request,"sorry, you can't change or remove another user's list")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

desc=[signin_required,owner_permission_required]

class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registeration successfull")
            return redirect("signin")
        else:
            print("failed")
            return render(request,"register.html",{"form":form})
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=SignInForm()
        return render(request,"signin.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=SignInForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                
                return redirect("index")
        
        print("form invalid")
        return render(request,"signin.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):  
        logout(request)
        messages.success(request,"successfully signout, see you next time")
        return redirect("signin")

@method_decorator(signin_required,name="dispatch")    
class IndexView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        qs=Todos.objects.filter(user=request.user).order_by("status")
        return render(request,"index.html",{"form":form,"data":qs})
    
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:
            return render(request,"index.html",{"form":form})

@method_decorator(desc,name="dispatch")       
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.filter(id=id).delete()
        return redirect("index")


@method_decorator(desc,name="dispatch")
class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        # Todos.objects.filter(id=id).update(status=True)
        todos_object=Todos.objects.get(id=id)
        if todos_object.status == True:
            todos_object.status=False
            todos_object.save()
        else:
            todos_object.status=True
            todos_object.save()
        return redirect("index")