from .models import User


def get_user_from_id(user_id):
    print(user_id)
    user = User.objects.get(id=user_id)
    return user


def get_user_from_mail(email):
    user = User.objects.get(email=email)
    return user
