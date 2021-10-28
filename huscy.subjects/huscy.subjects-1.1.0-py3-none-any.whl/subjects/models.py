import uuid
from datetime import date
from enum import Enum

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from dateutil import relativedelta
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    city = models.CharField(_('City'), max_length=128)
    country = CountryField(_('Country'), default='DE')

    # c.f. http://en.wikipedia.org/wiki/Postal_codes
    zip_code = models.CharField(_('Zip code'), max_length=16)

    # street name & number + additional info
    street = models.CharField(_('Street'), max_length=255)

    def __str__(self):
        return f'{self.country}-{self.zip_code} {self.city}, {self.street}'

    class Meta:
        ordering = 'country', 'city', 'zip_code', 'street'
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


class Contact(models.Model):
    class GENDER(Enum):
        female = (0, _('female'))
        male = (1, _('male'))
        diverse = (2, _('diverse'))

    first_name = models.CharField(_('First name'), max_length=128)  # without middle names
    last_name = models.CharField(_('Last name'), max_length=128)  # without middle names

    # full name with prefixes (titles) and suffixes
    display_name = models.CharField(_('Display name'), max_length=255)

    gender = models.PositiveSmallIntegerField(_('Gender'), choices=[x.value for x in GENDER])

    date_of_birth = models.DateField(_('Date of birth'))

    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name=_('Address'))
    email = models.EmailField(_('Email'), blank=True, default='')
    phone_mobile = PhoneNumberField(_('Phone mobile'), blank=True, default='')
    phone_home = PhoneNumberField(_('Phone home'), blank=True, default='')
    phone_work = PhoneNumberField(_('Phone work'), blank=True, default='')
    phone_emergency = PhoneNumberField(_('Phone emergency'), blank=True, default='')

    def __str__(self):
        return f'{self.display_name}'

    class Meta:
        ordering = 'last_name', 'first_name'
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class Subject(models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4, editable=False)

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='+',
                                verbose_name=_('Contact'))
    guardians = models.ManyToManyField(Contact, blank=True, related_name='subjects',
                                       verbose_name=_('Guardians'))

    @property
    def age_in_months(self):
        delta = relativedelta.relativedelta(date.today(), self.contact.date_of_birth)
        return delta.years * 12 + delta.months

    @property
    def age_in_years(self):
        return relativedelta.relativedelta(date.today(), self.contact.date_of_birth).years

    @property
    def is_active(self):
        # I used inactivity.all() instead of inactivity.get() because .get() would make extra
        # database queries
        inactivity = self.inactivity_set.all()
        if inactivity and (inactivity[0].until is None or inactivity[0].until >= date.today()):
            return False
        return True

    @property
    def is_child(self):
        return self.child_set.exists()

    @property
    def is_patient(self):
        return self.patient_set.exists()

    def __str__(self):
        return str(self.contact)

    class Meta:
        ordering = 'contact__last_name', 'contact__first_name'
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')


class Child(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Subject'))

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = 'subject__contact__last_name', 'subject__contact__first_name'
        verbose_name = _('Child')
        verbose_name_plural = _('Children')


class Patient(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Subject'))

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = 'subject__contact__last_name', 'subject__contact__first_name'
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')


class Note(models.Model):
    class OPTIONS(Enum):
        hard_of_hearing = (0, _('Hard of hearing'))
        hard_to_understand = (1, _('Hard to understand'))
        other = (255, _('Other'))

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes',
                                verbose_name=_('Subject'))
    option = models.PositiveSmallIntegerField(_('Option'), choices=[x.value for x in OPTIONS])
    text = models.TextField(_('Text'), blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                verbose_name=_('Creator'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        ordering = 'subject__contact__display_name', '-created_at'
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')


class Inactivity(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Subject'))
    until = models.DateField(_('Until'), null=True)  # until = null means inactive with open end

    class Meta:
        ordering = 'subject__contact__display_name',
        verbose_name = _('Inactivity')
        verbose_name_plural = _('Inactivities')
