from django.shortcuts import render, redirect
from . import models
import cv2
from imutils import url_to_image

face_cascade = cv2.CascadeClassifier('/haarcascade_frontalface_default.xml')

def index(request):
    if request.method == 'POST':

        url = models.Url.objects.create(
            image_url=request.POST.get('image_url', ''))
   
        img = url_to_image(request.POST.get('image_url', ''))
        ih, iw, _ = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        url.save()

        for (x, y, w, h) in faces:
            top = round(y * 100 / ih, 2)
            right = round((iw - x - w) * 100 / iw, 2)
            left = round(x * 100 / iw, 2)
            bottom = round((ih - y - h) * 100 / ih, 2)
            bb = models.BoundingBox.objects.create(top=top,
                                                   right=right,
                                                   left=left,
                                                   bottom=bottom,
                                                   image=url)
            bb.save()

        return redirect('/face')

    urls = models.Url.objects.all()

    context = {'image_urls': urls}
    return render(request, 'face/index.html', context)
