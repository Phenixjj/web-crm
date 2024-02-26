from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from sales.models import Customer, Order

from .decorators import user_not_authenticated
from .forms import LoginForm, SignUpForm
from .token import account_activation_token


# Create your views here.


def home(request):
    return render(request, 'base.html')


@user_not_authenticated
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save in the memory not in the database
            user.is_active = False
            user.save()
            # Get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('website/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            # Authenticate the user
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(request, username=username, password=password)
            # login(request, user)
            # return redirect('home')
    else:
        form = SignUpForm()
        # return render(request, 'website/register.html', {'form': form})
    return render(request, 'website/register.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully')
        return redirect('dashboard')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


@user_not_authenticated
def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.success(request, 'Username OR password is incorrect')
    else:
        form = LoginForm()
        messages.success(request, 'You have to resolve captcha first.')
        print("resolve captcha first.")
    return render(request, 'website/login.html', {'form': form})


def dashboard(request):
    # Fetch the last order for the logged-in user
    last_order = Order.objects.order_by('-date_created').first()

    # Fetch the sales data for all products
    product_sales = Order.objects.all().values('product__name').annotate(total_sales=Sum('quantity'))
    products_types_order = Order.objects.all().values('product__name').annotate(total_order=Count('product'))

    products, sales = [], []
    for i in product_sales:
        products.append(i['product__name'])
        sales.append(i['total_sales'])
    product_order = []

    for i in products_types_order:
        product_order.append(i['total_order'])

    return render(request, 'website/dashboard.html',
                  dict(last_order=last_order, products=products, sales=sales, product_order=product_order))
