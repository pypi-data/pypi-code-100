from .models import BannerTotalClicks, BannerViews
from rest_framework import serializers

class BannerTotalCliksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BannerTotalClicks
        fields = []

class BannerViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BannerViews
        fields = []
