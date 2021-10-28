from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import BannerViews, Banner, BannerTotalClicks, BannerClicks, BannerStatistics
from icecream import ic
from model_bakery import baker


class BannerTests(APITestCase):

    def setUp(self):
        self.banner = baker.make(Banner)

    def test_create_view_payload_for_existing_banner(self):
        """
        No Banner object created
        """
        url = reverse('banners-api:view', args=[self.banner.pk])              
        response = self.client.post(url, format='json')        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BannerStatistics.objects.count(), 1)
                    
    def test_create_view_payload_for_non_existing_banner(self):
        """
        Banner object exits
        """
        n_banner = self.banner.pk + 1        
        url = reverse('banners-api:view', args=[n_banner])              
        response = self.client.post(url, format='json')        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(BannerStatistics.objects.count(), 0)

    
    def test_create_click_payload(self):
        url = reverse('banners-api:save_click', args=[self.banner.pk])      
        data = {
            'url' : 'https://reaktion.se'
        }
        response = self.client.post(url, data, format='json')     
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BannerClicks.objects.count(), 1)
        self.assertEqual(BannerStatistics.objects.count(), 1)


    def test_create_click_payload_for_non_existing_banner(self):
        false_banner = self.banner.pk + 1        
        url = reverse('banners-api:save_click', args=[false_banner])      
        data = {
            'url' : 'https://reaktion.se'
        }        
        response = self.client.post(url, data, format='json')     
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(BannerClicks.objects.count(), 0)
        self.assertEqual(BannerStatistics.objects.count(), 0)


