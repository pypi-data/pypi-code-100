from datetime import datetime
import pytz
from django.utils.text import slugify

from django.shortcuts import render
from django.shortcuts import redirect

from .models import Banner

# Redirect and save click
def redirect_to_banner_target(request, pk):
    try:
        redirect_object = Banner.objects.get(pk=pk)
    except:
        return redirect('post:home')

    list_categories = ['Banner']
    list_tags = ['{}'.format(slugify(redirect_object.title))]

    redirect_object.save_click()
    return render(request, 'banner/banner.html',
                  {'url': redirect_object.image_url, 'catgs': list_categories, 'tags': list_tags})

    #redirect_object.save_click()
    #return redirect(redirect_object.image_url)