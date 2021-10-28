from django.db import models
from django.utils.timezone import now
import datetime


class Banner(models.Model):

    TOP = 'TOP'
    SIDEBAR_RIGHT = 'SDR'
    SIDEBAR_LEFT = 'SDL'
    CONTENT = 'CON'
    BOTTOM = 'BOT'
    BANNER_CHOICES = (
        (TOP, 'Top'),
        (SIDEBAR_RIGHT, 'Sidebar Right'),
        (SIDEBAR_LEFT, 'Sidebar Left'),
        (CONTENT, 'Content'),
        (BOTTOM, 'Bottom'),
    )
    title = models.CharField(max_length=200, verbose_name="Title", default='')
    impressions = models.IntegerField(verbose_name="Impressions", default=0)
    views = models.IntegerField(verbose_name="Visningar", default=0)
    clicks = models.IntegerField(verbose_name="Klicks", default=0)
    published = models.DateTimeField(verbose_name = "Publicerat", default=now)
    valid_until = models.DateTimeField(verbose_name = "Giltig till", default=now)
    image = models.ImageField(verbose_name="Banner", upload_to="banner", null=True, blank=True)
    image_url = models.CharField(max_length=200, verbose_name="Banner url", null=True, blank=True)
    #code = models.TextField(verbose_name="Koden", default='', blank=True)
    #code_mobile = models.TextField(verbose_name="Koden - mobilen", default='', blank=True)
    position = models.CharField(
        max_length=3,
        choices=BANNER_CHOICES,
        default=TOP,
    )
    order = models.IntegerField(verbose_name="Ordning", default=1)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['-created']

    def save_impression(self):
        self.impressions = self.impressions + 1;
        self.save()

    def save_click(self):
        self.clicks = self.clicks + 1
        self.save()

    def __str__(self):
        return self.title


class BannerImpressions(models.Model):

    banner_id = models.ForeignKey(Banner, on_delete=models.CASCADE, default=0)
    date = models.DateField(verbose_name="datum", default=now)
    count = models.IntegerField(verbose_name="Impressions", default=0)

    class Meta:
        verbose_name = "Banner Impressions"
        verbose_name_plural = "Banner Impressions"
        ordering = ['-date']

    def save_impression(self):
        self.impressions = self.impressions + 1;
        self.save()

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class BannerViews(models.Model):
    
    banner_id = models.ForeignKey(Banner, on_delete=models.CASCADE, default=0)
    date = models.DateField(verbose_name="datum", default=now)
    count = models.IntegerField(verbose_name="Visningar", default=0)

    class Meta:
        verbose_name = "Banner Visning"
        verbose_name_plural = "Banner Visningar"
        ordering = ['-date']

    def save_view(self):
        self.views = self.views + 1;
        self.save()

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class BannerTotalClicks(models.Model):

    banner_id = models.ForeignKey(Banner, on_delete=models.CASCADE, default=0)
    count = models.IntegerField(verbose_name="Klicks", default=0)
    date = models.DateField(verbose_name="datum", default=now)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = "Banner Total Click"
        verbose_name_plural = "Banner Total Clicks"
        ordering = ['-date']

    def save_click(self):
        self.clicks = self.clicks + 1
        self.save()

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

class BannerStatistics(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.PROTECT, null=True)
    date = models.DateField(verbose_name="datum", default=now)
    impressions = models.IntegerField(verbose_name="Impressions", default=0)
    views = models.IntegerField(verbose_name="Views", default=0)
    clicks = models.IntegerField(verbose_name="Clicks", default=0)

    class Meta:
        verbose_name = "Banner Statistic"
        verbose_name_plural = "Banner Statistics"
        ordering = ['-date']

    @classmethod
    def save_impression(self, banner):
        now = datetime.date.today()                 
        banner_view, created = self.objects.get_or_create(
            date=now, 
            banner=banner, 
            defaults={ 'views': 0, 'clicks' : 0, 'impressions' : 1 } )
            
        if created is False:
            banner_view.impressions = banner_view.impressions + 1
            banner_view.save()
    
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class BannerClicks(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.PROTECT, null=True)
    url = models.URLField(verbose_name="URL", default='')
    full_url = models.URLField(verbose_name="URL", default='')
    date = models.DateField(verbose_name="datum", default=now)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = "Banner Click"
        verbose_name_plural = "Banner Clicks"
        ordering = ['-date']

    def save_click(self):
        self.clicks = self.clicks + 1
        self.save()

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
