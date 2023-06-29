from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login,authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CustomUserCreationForm, LoginForm

def SignUpView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is inactive until email is confirmed
            user.save()
            
            # Email confirmation
            
            host_name = request.get_host() 
            uid = urlsafe_base64_encode(force_bytes(user.pk)) 
            token = default_token_generator.make_token(user) 
            activation_link = f"{request.scheme}://{host_name}{reverse('activate_account', kwargs={'uidb64': uid, 'token': token})}" 
            print(activation_link)
            email_html_message = render_to_string('registration/activation_email.html', { 
                'user': user, 
                'activation_link':activation_link, 
            }) 
            # Send the activation email 
            email = EmailMessage( 
                'Account Activation', 
                email_html_message, 
                from_email='team@filserver.com', 
                to=[user.email], 
                 
            )
            email.content_subtype = 'html'
            email.send()
            messages.info(request, 'Signup successful, kindly check your email for activation link')
            return redirect('login')          
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account Activated. You can now login")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link")
        return redirect("login")
    
def login_View(request):
    
    if request.user.is_authenticated:
        return redirect('list')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email =  form.cleaned_data['email']
            password = form.cleaned_data['password']
            user= authenticate(request,email=email, password=password) # Verification of user credentials
            
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('list')
                messages.info(request, "Kindly activate your Email,check your email for your activation link")    
                return redirect('login')
            messages.error(request, "Wrong Email or Password")
            return redirect('login')
    else:
        form= LoginForm()
    return render(request,'registration/login.html',{'form':form})
                