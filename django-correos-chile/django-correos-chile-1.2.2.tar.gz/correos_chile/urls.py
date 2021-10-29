from django.urls import path

from .views import get_c128_barcode


urlpatterns = [
    path('barcode/<str:ccl_enc>/<str:shipping_nbr>/<int:slip>/c128/',
        get_c128_barcode, name='barcode-c128'),
]