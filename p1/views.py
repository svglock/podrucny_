from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import User
from .forms import RegisterForm, UserProfileForm, SupplierProfileForm, CourierProfileForm, ReviewForm
from django.urls import reverse


# @login_required
# def user_reviews(request, user_id):
#     target_user = get_object_or_404(User, id=user_id)
#     avg = target_user.get_average_rating()
#     avg_rounded = round(avg * 2) / 2
#     reviews = target_user.reviews_received.all().order_by('-created_at')
#     # Проверка, оставлял ли уже отзыв этот пользователь
#     already_reviewed = Review.objects.filter(from_user=request.user, to_user=target_user).exists()
#     can_review = (request.user != target_user) and not already_reviewed
#
#     if request.method == 'POST' and can_review:
#         form = ReviewForm(request.POST, request.FILES)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.from_user = request.user
#             review.to_user = target_user
#             review.save()
#             messages.success(request, 'Отзыв добавлен!')
#             return redirect('user_reviews', user_id=user_id)
#     else:
#         form = ReviewForm() if can_review else None
#
#     return render(request, 'user_reviews.html', {
#         'target_user': target_user,
#         'reviews': reviews,
#         'form': form,
#         'already_reviewed': already_reviewed,
#         'avg_rating': avg_rounded
#     })


@login_required
def send_verification(request):
    user = request.user
    if user.email_verified:
        messages.info(request, 'Email уже подтверждён.')
        return redirect('profile')
    # Генерируем токен
    import random, string
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    user.email_verification_token = token
    user.save()
    # Временно показываем ссылку прямо в интерфейсе
    verify_link = request.build_absolute_uri(reverse('verify_email', args=[token]))
    messages.success(request, f'Ссылка для подтверждения: {verify_link}')
    return redirect('profile')


def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)
    user.email_verified = True
    user.email_verification_token = ''
    user.save()
    login(request, user)
    messages.success(request, 'Email подтверждён!')
    return redirect('profile')


def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'customer':
            return redirect('select_product')
        elif request.user.role == 'supplier':
            return redirect('supplier_orders')
        elif request.user.role == 'courier':
            return redirect('courier_orders')
    else:
        return redirect('login')  # страница входа


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('profile')   # или 'home'
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def welcome(request):
    return HttpResponse(f"Добро пожаловать, {request.user.username}!")


# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'products.html', {'products': products})
#
#
# def supplier_list(request):
#     suppliers = SupplierProfile.objects.all()
#     search = request.GET.get('search', '')
#     if search:
#         suppliers = suppliers.filter(
#             Q(company_name__icontains=search) | Q(user__username__icontains=search)
#         )
#
#     region = request.GET.get('region', '')
#     if region:
#         suppliers = suppliers.filter(region__icontains=region)
#     city = request.GET.get('city', '')
#     if city:
#         suppliers = suppliers.filter(city__icontains=city)
#
#     has_own_delivery = request.GET.get('has_own_delivery')
#     allow_pickup = request.GET.get('allow_pickup')
#
#     if has_own_delivery == 'on':
#         suppliers = suppliers.filter(has_own_delivery=True)
#     if allow_pickup == 'on':
#         suppliers = suppliers.filter(allow_pickup=True)
#
#     # Обработка рейтинга: вначале пробуем radio-кнопки, затем кастомное поле
#     # Обработка рейтинга
#     min_rating = request.GET.get('min_rating', '')
#     if min_rating:
#         try:
#             rating_val = float(min_rating)
#             suppliers = [s for s in suppliers if s.user.get_average_rating() >= rating_val]
#         except ValueError:
#             pass
#
#     # Обработка суммы заказа
#     max_min_order = request.GET.get('max_min_order', '')
#     if max_min_order:
#         try:
#             val = float(max_min_order)
#             suppliers = [s for s in suppliers if s.min_order_amount <= val]
#         except ValueError:
#             pass
#
#     context = {
#         'suppliers': suppliers,
#         'search_query': search,
#         'region': region,
#         'city': city,
#         'has_own_delivery_checked': has_own_delivery == 'on',
#         'allow_pickup_checked': allow_pickup == 'on',
#         'min_rating': min_rating,  # для кастомного поля
#         'max_min_order': max_min_order
#     }
#     return render(request, 'suppliers.html', context)


# def courier_list(request):
#     couriers = CourierProfile.objects.all()
#
#     search = request.GET.get('search', '')
#     region = request.GET.get('region', '')
#     vehicle_type = request.GET.get('vehicle_type', '')
#     has_loaders = request.GET.get('has_loaders')
#     min_rating = request.GET.get('min_rating', '')
#     min_weight = request.GET.get('min_weight', '')
#     min_volume = request.GET.get('min_volume', '')
#
#     if search:
#         couriers = couriers.filter(user__username__icontains=search)
#     if region:
#         couriers = couriers.filter(region__icontains=region)
#     if vehicle_type:
#         couriers = couriers.filter(vehicle_type=vehicle_type)
#     if has_loaders == 'on':
#         couriers = couriers.filter(has_loaders=True)
#
#     # Фильтр по весу
#     if min_weight:
#         try:
#             couriers = couriers.filter(max_weight_kg__gte=float(min_weight))
#         except ValueError:
#             pass
#
#     # Фильтр по объёму
#     if min_volume:
#         try:
#             couriers = couriers.filter(cargo_volume_m3__gte=float(min_volume))
#         except ValueError:
#             pass
#
#     # Фильтр по рейтингу (в Python, т.к. рейтинг вычисляемый)
#     if min_rating:
#         try:
#             rating_val = float(min_rating)
#             couriers = [c for c in couriers if c.user.get_average_rating() >= rating_val]
#         except ValueError:
#             pass
#
#     context = {
#         'couriers': couriers,
#         'search_query': search,
#         'region': region,
#         'selected_vehicle': vehicle_type,
#         'vehicle_types': CourierProfile.VEHICLE_TYPE_CHOICES,
#         'has_loaders_checked': has_loaders == 'on',
#         'min_rating': min_rating,
#         'min_weight': min_weight,
#         'min_volume': min_volume,
#     }
#     return render(request, 'couriers.html', context)
#
#
# def select_product(request):
#     products = Product.objects.all()
#     selected_product = None
#     suppliers = []
#     couriers = []
#     quantity = 1
#     total_weight = 0
#     total_volume = 0
#
#     if request.method == 'POST':
#         product_id = request.POST.get('product')
#         quantity = int(request.POST.get('quantity', 1))
#         selected_product = Product.objects.get(id=product_id)
#
#         total_weight = selected_product.weight * quantity
#         total_volume = selected_product.get_volume() * quantity
#
#         suppliers = SupplierProfile.objects.filter(products=selected_product)
#         couriers = CourierProfile.objects.all()
#
#         if selected_product.requires_cold:
#             couriers = couriers.filter(has_fridge=True)
#
#         couriers = couriers.filter(
#             max_weight_kg__gte=total_weight,
#             cargo_volume_m3__gte=total_volume
#         )
#
#     return render(request, 'select_product.html', {
#         'products': products,
#         'selected_product': selected_product,
#         'suppliers': suppliers,
#         'couriers': couriers,
#         'quantity': quantity,
#         'total_weight': total_weight,
#         'total_volume': total_volume,
#     })


# def public_profile(request, user_id):
#     profile_user = get_object_or_404(User, id=user_id)
#     context = {'profile_user': profile_user}
#     if profile_user.role == 'supplier':
#         try:
#             supplier = profile_user.supplier_profile
#             context['supplier'] = supplier
#             context['products'] = supplier.products.all()
#         except SupplierProfile.DoesNotExist:
#             pass
#     elif profile_user.role == 'courier':
#         try:
#             context['courier'] = profile_user.courier_profile
#         except CourierProfile.DoesNotExist:
#             pass
#     # для заказчика просто показываем контакты
#     return render(request, 'public_profile.html', context)
#
#
# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         user_form = UserProfileForm(request.POST, request.FILES, instance=user)
#         if user.role == 'supplier':
#             profile, created = SupplierProfile.objects.get_or_create(user=user)
#             profile_form = SupplierProfileForm(request.POST, instance=profile)
#         elif user.role == 'courier':
#             profile, created = CourierProfile.objects.get_or_create(user=user)
#             profile_form = CourierProfileForm(request.POST, instance=profile)
#         else:
#             profile_form = None
#
#         if user_form.is_valid():
#             user_form.save()
#             if profile_form and profile_form.is_valid():
#                 profile_form.save()
#             messages.success(request, 'Профиль обновлён')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Пожалуйста, исправьте ошибки')
#     else:
#         user_form = UserProfileForm(instance=user)
#         if user.role == 'supplier':
#             try:
#                 profile = user.supplier_profile
#                 profile_form = SupplierProfileForm(instance=profile)
#             except SupplierProfile.DoesNotExist:
#                 profile_form = SupplierProfileForm()
#         elif user.role == 'courier':
#             try:
#                 profile = user.courier_profile
#                 profile_form = CourierProfileForm(instance=profile)
#             except CourierProfile.DoesNotExist:
#                 profile_form = CourierProfileForm()
#         else:
#             profile_form = None
#
#     return render(request, 'profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#     })
#
#
# @login_required
# @login_required
# def supplier_orders(request):
#     if request.user.role != 'supplier':
#         return redirect('home')
#     try:
#         profile = request.user.supplier_profile
#     except SupplierProfile.DoesNotExist:
#         return redirect('profile')
#     orders = Order.objects.filter(supplier=profile).order_by('-created_at')
#     return render(request, 'supplier_orders.html', {
#         'orders': orders,
#         'STATUS_CHOICES': Order.STATUS_CHOICES,   # передаём список статусов
#     })
#
#
# @login_required
# def courier_orders(request):
#     if request.user.role != 'courier':
#         return redirect('home')
#     try:
#         profile = request.user.courier_profile
#     except CourierProfile.DoesNotExist:
#         return redirect('profile')
#     orders = Order.objects.filter(courier=profile).order_by('-created_at')
#     return render(request, 'courier_orders.html', {'orders': orders})
#
#
# @login_required
# def update_order_status(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     # Проверка прав
#     if request.user.role == 'supplier' and order.supplier and order.supplier.user == request.user:
#         pass
#     elif request.user.role == 'courier' and order.courier and order.courier.user == request.user:
#         pass
#     else:
#         return redirect('home')
#
#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         if new_status in dict(Order.STATUS_CHOICES).keys():
#             order.status = new_status
#             order.save()
#     return redirect(request.META.get('HTTP_REFERER', '/'))
