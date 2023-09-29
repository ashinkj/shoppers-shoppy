from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,AddressUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

UserModel = get_user_model()
from .tokens import account_activation_token

from store.models import ShippingAddress,Customer
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            form.save()

            customer = Customer(user=user, name=user.username, email=user.email)
            customer.save()
            username = form.cleaned_data.get('username')
            email = request.POST.get('email')
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('user/activite.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            
            messages.success(request, f'Please confirm your email address to complete the registration')
            return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Your account has been created! You are now able to log in')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('your_name')
        password = request.POST.get('your_pass')
        

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store-page')
        else:
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'user/login.html')  


@login_required
def profile(request):
    user = request.user

    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        # If the customer doesn't exist, create one
        customer = Customer(user=user, name=user.username, email=user.email)
        customer.save()

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # If the profile doesn't exist, create one
        profile = Profile(user=user)
        profile.save()

    try:
        shipping_address = ShippingAddress.objects.get(customer=customer)
    except ShippingAddress.DoesNotExist:
        # If the shipping address doesn't exist, initialize it as None
        shipping_address = None

    u_form = UserUpdateForm(instance=user)
    p_form = ProfileUpdateForm(instance=profile)
    a_form = AddressUpdateForm(instance=shipping_address) if shipping_address else None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if a_form:
            a_form = AddressUpdateForm(request.POST, instance=shipping_address) if shipping_address else None

        if u_form.is_valid() and p_form.is_valid() and (not a_form or a_form.is_valid()):
            u_form.save()
            p_form.save()

            if a_form:
                a_form.save()
                messages.success(request, 'Your Profile has been updated!')

            return redirect('profile')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'a_form': a_form,
    }

    return render(request, 'user/profile.html', context)