from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count

import csv
from datetime import datetime, timedelta

from .models import Banner, BannerClicks, BannerStatistics


class BannerAdmin(admin.ModelAdmin):
    readonly_fields = ('impressions', 'views', 'clicks', 'updated', 'created')
    list_display = ('title', 'valid_until','position', 'order', 'clicks')
    fields = (
        'title',
        'position',
        'published',
        'valid_until',
        'image',
        'image_url',
        'order'
    )

    actions = ['download_banner_statistics', 'download_banner_clicks']

    def download_banner_clicks(self, request, queryset):
        banner_id = request.POST['_selected_action']

        banner = Banner.objects.get(pk=banner_id)

        filename = "Banner-{}".format(banner.title)

        bc = BannerClicks.objects.filter(banner=banner_id)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(filename)
        writer = csv.writer(response)

        writer.writerow(['Datum', 'Clicks'])
        for obj in bc:            
            row = writer.writerow([obj.date, obj.url ])
            
        return response


    def download_banner_statistics(self, request, queryset):

        banner_id = request.POST['_selected_action']

        bs = BannerStatistics.objects.filter(banner=banner_id)
        banner = Banner.objects.get(pk=banner_id)

        filename = "Banner-{}".format(banner.title)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(filename)
        writer = csv.writer(response)

        writer.writerow(['Datum', 'Impressions', 'Views', '%', 'Clicks', '%'])
        for obj in bs:
            v_i = round((obj.views/obj.impressions) * 100)
            c_v = round((obj.clicks/obj.views) * 100)
            row = writer.writerow([obj.date, obj.impressions, obj.views, "{} %".format(v_i), obj.clicks, "{} %".format(c_v)])
            
        return response

    download_banner_statistics.short_description = "Ladda ner banner statistiken"
    download_banner_clicks.short_description = "Ladda ner banners alla klickar"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        how_many_days = 14

        better_bc = BannerClicks.objects.filter(banner_id=object_id).filter(date__gte=datetime.now()-timedelta(days=how_many_days)).values('url').annotate(total=Count('url')).order_by('-total')
        extra_context['better_bc'] = better_bc

        banner_statistics = BannerStatistics.objects.filter(banner_id=object_id).filter(date__gte=datetime.now()-timedelta(days=how_many_days)).order_by('-date')
        extra_context['banner_statistics'] = banner_statistics

        all_impressions = 0
        all_views = 0
        all_clicks = 0

        for element in banner_statistics:
            all_impressions = all_impressions + element.impressions
            all_views = all_views + element.views
            all_clicks = all_clicks + element.clicks

        if all_impressions == 0:
            v_i = 0
        else:
            v_i = round((all_views/all_impressions)*100)
        
        if all_views == 0:
            v_c = 0
        else:
            v_c = round((all_clicks/all_views)*100)

        summary = {
            'impressions' : all_impressions,
            'v_i' : v_i,
            'views' : all_views,
            'v_c' : v_c,
            'clicks' : all_clicks
        }

        extra_context['summary'] = summary
        extra_context['how_many_days'] = how_many_days

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )



admin.site.register(Banner, BannerAdmin)