from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import reverse

def SignUpView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is inactive until email is confirmed
            user.save()
            
            # Email confirmation
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            
            activation_url = reverse('activate_account', args=[urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user)])
    
            return redirect(activation_url)
            
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
        user.is_email_confirmed = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')
