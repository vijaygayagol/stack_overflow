from django.shortcuts import render,redirect
from users.forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.models import User

# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_create.html'
    success_url = '/index/'

def profile(request):
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm( instance=request.user)
        p_form = ProfileUpdateForm( instance=request.user.profile)
    context={
        "u_form":u_form,
        "p_form":p_form}
    return render(request,'users/profile.html',context)
