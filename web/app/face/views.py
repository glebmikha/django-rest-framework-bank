from django.shortcuts import render, redirect
from . import models


def index(request):
    if request.method == 'POST':

        url = models.Url.objects.create(
            image_url=request.POST.get('image_url', ''))

        url.save()

        return redirect('/face')

    urls = models.Url.objects.all()

    context = {'image_urls': urls}
    return render(request, 'face/index.html', context)
