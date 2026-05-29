from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


#@admin.register(Vehicle)
#class VehicleAdmin(admin.ModelAdmin):
#   list_display = ['courier', 'vehicle_type', 'model_name', 'max_weight_kg']


#@admin.register(Driver)
#class DriverAdmin(admin.ModelAdmin):
#    list_display = ['full_name', 'courier', 'experience_years', 'license_categories']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'phone', 'is_verified']
    list_filter = ['role', 'is_verified']
    fieldsets = UserAdmin.fieldsets + (
        ('Доп. информация', {'fields': ('role', 'phone', 'social_link', 'is_verified')}),
    )


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'category', 'weight', 'requires_cold', 'requires_fragile']
#     list_filter = ['category', 'requires_cold', 'requires_fragile']
#     search_fields = ['name']
#
#
# @admin.register(SupplierProfile)
# class SupplierProfileAdmin(admin.ModelAdmin):
#     list_display = ['company_name', 'user', 'region', 'has_cold_storage']
#     list_filter = ['region', 'has_cold_storage']
#
#
# @admin.register(CourierProfile)
# class CourierProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'region', 'max_weight_kg', 'cargo_volume_m3', 'has_fridge']
#     list_filter = ['region', 'has_fridge']
#
#
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 1
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'customer', 'supplier', 'courier', 'status', 'created_at']
#     list_filter = ['status', 'created_at']
#     inlines = [OrderItemInline]
#
#
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['from_user', 'to_user', 'rating', 'created_at']
#     list_filter = ['rating']
