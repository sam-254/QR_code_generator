from django.shortcuts import render
import qrcode
import qrcode.image.svg
from io import BytesIO
from .models import QrCode
from django.http import HttpResponse

def index(request):
    context = {}
    if request.method == "POST":
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(request.POST.get("qr_text",""), image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()

    return render(request, "index.html", context=context)


# def editProfile(request):
#     if request.method == 'POST':
#         profilePicture = request.FILES['pp']
#         if request.user.about:
#             request.user.about.profilePicture=profilePicture
#             request.user.about.save()

#             return