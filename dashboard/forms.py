from accounts.models import User
from django import forms
from orders.models import Company
from warehouse.models import Product


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class CreateOrderForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label='Товар',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    quantity = forms.IntegerField(
        min_value=1,
        label='Количество',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество'
            }
        )
    )
    customer_company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        label='Компания',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )


class ExcelImportForm(forms.Form):
    file = forms.FileField()


class XMLImportForm(forms.Form):
    file = forms.FileField()


from orders.models import Order


class CreateDeliveryForm(forms.Form):
    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),
    label = 'Заказ',
    widget = forms.Select(
        attrs={
            'class': 'form-select'
        }
    )
    )

    courier = forms.ModelChoiceField(
        queryset=User.objects.filter(
            role='courier'
        ),
        label='Курьер',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
    route_duration_minutes = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=0
    )
    start_address = forms.CharField(
        label='Адрес отправления',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите адрес отправления'
        })
    )

    end_address = forms.CharField(
        label='Адрес доставки',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите адрес доставки'
        })
    )
    distance_km = forms.DecimalField(
        decimal_places=2,
        max_digits=10,
        label='Расстояние (км)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }
        )
    )
