from django.shortcuts import render
from . import models


def index(request):
    if request.method == 'POST':
        print(request.POST.get('image_url', ''))

        url = models.Url.objects.create(
            image_url=request.POST.get('image_url', ''))
    
        url.save()


    urls = models.Url.objects.all()

    context = {'image_urls': urls}
    return render(request, 'face/index.html', context)
