from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import datetime

from .models import BannerViews, Banner, BannerTotalClicks, BannerClicks, BannerStatistics
from .serializers import BannerViewsSerializer, BannerTotalCliksSerializer


class API_BannerView(APIView):
    http_method_names = [ 'post', 'head' ]

    def post(self, request, banner_id, format=None):
        serializer = BannerViewsSerializer(data=request.data)
        if serializer.is_valid():       
            try:
                banner = Banner.objects.get(pk=banner_id)            
                now = datetime.date.today() 
                banner_view, created = BannerStatistics.objects.get_or_create(date=now, banner=banner, defaults={ 'views': 0, 'clicks' : 0, 'impressions' : 0 } )
                if created is False:
                    banner_view.views = banner_view.views + 1
                    banner_view.save()                              
            except ObjectDoesNotExist:
                return Response({"status" : "Banner does not exist."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class API_BannerTotalClicks(APIView):
    http_method_names = ['post', 'head' ]

    def post(self, request, banner_id, format=None):
        serializer = BannerTotalCliksSerializer(data=request.data)    
        if serializer.is_valid():   
            
            try:
                """
                Add to BannerClicks
                """
                now = datetime.date.today() 
                banner = Banner.objects.get(pk=banner_id)             

                """Add to BannerTotalClicks
                """                        
                banner_view, created = BannerStatistics.objects.get_or_create(date=now, banner=banner, defaults={ 'views': 0, 'clicks' : 0, 'impressions' : 0 } )
                if created is False:
                    banner_view.clicks = banner_view.clicks + 1
                    banner_view.save()     

                
                """ Add to BannerClicks"""
                BannerClicks.objects.create(
                    banner_id=banner.id,
                    url=request.data['url'],
                    full_url=request.data['full_url'],
                    date=now
                )

            except ObjectDoesNotExist:
                return Response({"status" : "Banner does not exist."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            


