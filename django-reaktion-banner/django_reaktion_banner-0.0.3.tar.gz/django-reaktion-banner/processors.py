from .models import Banner, BannerStatistics
import datetime
import random
from django.urls import reverse
from icecream import ic
import os


today = datetime.date.today()


def banner_endpoint(request):
    return { 'BANNERS_ENDPOINT' : os.environ['BANNERS_ENDPOINT'] }

def banner_top(request):
    """
    Return random banners for the top
    :param request:
    :return:
    """
    if request.path.startswith(reverse('admin:index')):
        return {'banner_top': ''}

    else:

        banners = Banner.objects.filter(position__exact="TOP").filter(valid_until__gte=today).all().order_by("?")
        if banners:
            ic(banners)
            if len(banners) > 1:
                banner = random.choice(banners)
                return {'banner_top': banner}
            else:
                return {'banner_top': banners}
            """
            Save to statistics (impressions)
            """
            #BannerStatistics.save_impression(banner)

        else:
            return {'banner_top': ''}


def banner_sidebar_right(request):
    """
    Return random banners for the right sidebar
    :param request:
    :return:
    """
    if request.path.startswith(reverse('admin:index')):
        return {'banner_sidebar_right': ''}

    else:

        banners = Banner.objects.filter(position__exact="SDR").filter(valid_until__gte=today).all().order_by("?")
        if banners:
            ic(banners)
            if len(banners) > 1:
                banner = random.choice(banners)
            
                return {'banner_sidebar_right': banner}
            else:
                return {'banner_sidebar_right': banners}
            """
            Save to statistics (impressions)
            """
            #BannerStatistics.save_impression(banner)

        else:
            return {'banner_siderbar_right': ''}


def banner_sidebar_left(request):
    """
    Return random banners for the left sidebar
    :param request:
    :return:
    """
    if request.path.startswith(reverse('admin:index')):
        return {'banner_sidebar_left': ''}

    else:

        banners = Banner.objects.filter(position__exact="SDL").filter(valid_until__gte=today).all().order_by("?")
        if banners:
            ic(banners)
            if len(banners) > 1:
                banner = random.choice(banners)
                return {'banner_sidebar_left': banner}
            else:
                return {'banner_sidebar_left': banners}
            """
            Save to statistics (impressions)
            """
            #BannerStatistics.save_impression(banner)

        else:
            return {'banner_siderbar_left': ''}


def banner_content(request):
    """
    Return random banners for content location
    :param request:
    :return:
    """
    if request.path.startswith(reverse('admin:index')):
        return {'banner_sidebar_content': ''}

    else:

        banners = Banner.objects.filter(position__exact="CON").filter(valid_until__gte=today).all().order_by("?")
        if banners:
            ic(banners)
            if len(banners) > 1:
                banner = random.choice(banners)
                return {'banner_content': banner}
            else:
                return {'banner_content': banners}
            """
            Save to statistics (impressions)
            """
            #BannerStatistics.save_impression(banner)

        else:
            return {'banner_content': ''}


def banner_bottom(request):
    """
    Return random banners for the bottom of the page
    :param request:
    :return:
    """


    if request.path.startswith(reverse('admin:index')):
        return {'banner_bottom': ''}

    else:

        banners = Banner.objects.filter(position__exact="BOT").filter(valid_until__gte=today).all().order_by("?")
        if banners:
            ic(banners)
            if len(banners) > 1:
                banner = random.choice(banners)
                return {'banner_bottom': banner}
            else:
                return {'banner_bottom': banners}
            
            """
            Save to statistics (impressions)
            """
            #BannerStatistics.save_impression(banner)

        else:
            return {'banner_bottom': ''}





