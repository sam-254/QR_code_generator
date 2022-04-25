import qrcode
from django.conf import settings


def generate_user_qr(username, email, phone):
    data = f"{username} {email} {phone}"
    img = qrcode.make(data)
    path = f'{settings.MEDIA_ROOT}/{username}.png'
    url = f'{settings.MEDIA_URL}/{username}.png'
    img.save(path)
    return path, url
