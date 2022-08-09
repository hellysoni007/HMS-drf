from .models import User, Address


def get_user_from_id(user_id):
    print(user_id)
    user = User.objects.get(id=user_id)
    return user


def get_user_from_mail(email):
    user = User.objects.get(email=email)
    return user


def get_address_from_user_id(user_id):
    if Address.objects.filter(user=user_id).exists():
        return Address.objects.get(user=user_id)
