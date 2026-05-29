from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'social_link', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'social_link': forms.URLInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


# class SupplierProfileForm(forms.ModelForm):
#     class Meta:
#         model = SupplierProfile
#         fields = ['company_name', 'region', 'city', 'has_cold_storage',
#             'min_order_amount', 'has_own_delivery', 'allow_pickup', 'products',
#             'description', 'payment_terms',
#             'own_couriers',]
#         widgets = {
#             'company_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'region': forms.TextInput(attrs={'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'class': 'form-control'}),
#             'min_order_amount': forms.NumberInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'payment_terms': forms.TextInput(attrs={'class': 'form-control'}),
#             'products': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
#             'own_couriers': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
#         }
#
#
# class ReviewForm(forms.ModelForm):
#     rating = forms.FloatField(
#         min_value=0.5,
#         max_value=5.0,
#         widget=forms.HiddenInput(attrs={'id': 'rating-input'}),
#         label='Оценка'
#     )
#
#     class Meta:
#         model = Review
#         fields = ['rating', 'comment', 'image']
#         labels = {
#             'comment': 'Комментарий',
#             'image': 'Фото',
#         }
#         widgets = {
#             'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опишите ваш опыт...'}),
#             'image': forms.FileInput(attrs={'class': 'form-control'}),
#         }
#
#
# class CourierProfileForm(forms.ModelForm):
#     # поля-опции выводим как чекбоксы (в шаблоне мы их оформим красиво)
#     has_fridge = forms.BooleanField(label='❄️ Рефрижератор', required=False)
#     has_heat = forms.BooleanField(label='🔥 Тёплый бокс', required=False)
#     extra_packaging = forms.BooleanField(label='📦 Доп. упаковка', required=False)
#     animals_allowed = forms.BooleanField(label='🐾 Перевозка животных', required=False)
#
#     class Meta:
#         model = CourierProfile
#         fields = [
#             'region', 'max_weight_kg', 'cargo_volume_m3', 'has_fridge',
#             'has_heat', 'extra_packaging', 'animals_allowed',
#             'vehicle_type', 'has_loaders', 'available_days', 'price_per_km'
#         ]
#         labels = {
#             'region': 'Регион',
#             'max_weight_kg': 'Грузоподъёмность, кг',
#             'cargo_volume_m3': 'Объём кузова, м³',
#             'vehicle_type': 'Тип основного транспорта',
#             'has_loaders': 'Есть грузчики',
#             'available_days': 'Доступные дни',
#             'price_per_km': 'Цена за км',
#         }
#
#
# class CustomerProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomerProfile
#         fields = ['experience_years', 'description', 'preferred_categories']
#         widgets = {
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'preferred_categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
#         }
