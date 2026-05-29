from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSupplier(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'supplier'
        )


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'customer'
        )


class IsCourier(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'courier'
        )


class IsManager(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == 'manager'
                or request.user.role == 'admin'
                or request.user.is_staff
            )
        )


class IsOwnerOrManager(BasePermission):

    def has_object_permission(self, request, view, obj):

        if (
            request.user.role == 'manager'
            or request.user.role == 'admin'
            or request.user.is_staff
        ):
            return True

        if hasattr(obj, 'supplier'):
            return obj.supplier == request.user

        if hasattr(obj, 'customer'):
            return obj.customer == request.user

        if hasattr(obj, 'courier'):
            return obj.courier == request.user

        return False