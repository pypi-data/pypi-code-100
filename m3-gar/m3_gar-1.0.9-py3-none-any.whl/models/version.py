from django.db import (
    models,
)


__all__ = ['Version', 'Status']


class VersionManager(models.Manager):

    def nearest_by_date(self, date):
        return self.get_queryset().filter(dumpdate__lte=date).latest('dumpdate')


class Version(models.Model):

    objects = VersionManager()

    ver = models.IntegerField(primary_key=True)
    date = models.DateField(db_index=True, blank=True, null=True)
    dumpdate = models.DateField(db_index=True)

    complete_xml_url = models.CharField(max_length=255)
    delta_xml_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.ver} from {self.dumpdate}'


class Status(models.Model):

    table = models.CharField(primary_key=True, max_length=25)
    ver = models.ForeignKey(Version, on_delete=models.CASCADE)

    def __str__(self):
        return self.table
