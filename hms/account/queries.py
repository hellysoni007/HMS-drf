from .models import User, Address, Rooms


def get_user_from_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist as e:
        print(f'ERROR {e}')
        return None


def get_user_from_mail(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist as e:
        print(f'ERROR {e}')
        return None


def get_address_from_user_id(user_id):
    if Address.objects.filter(user=user_id).exists():
        return Address.objects.get(user=user_id)
    else:
        return None


def get_all_rooms():
    rooms = Rooms.objects.all()
    return rooms
