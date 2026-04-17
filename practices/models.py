import uuid

from django.db import models


class Practice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    tax_id = models.CharField(max_length=20, blank=True, default='')
    npi_number = models.CharField(max_length=10, blank=True, default='')

    def __str__(self):
        return self.name


class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    title = models.CharField(
        max_length=100, blank=True, default='Uncredentialed',
    )
    specialty = models.CharField(max_length=255)
    npi_credential = models.ForeignKey(
        'NpiCredential',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_providers',
    )
    dea_credential = models.ForeignKey(
        'DeaCredential',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_providers',
    )
    practices = models.ManyToManyField(
        Practice,
        through='ProviderByPractice',
        related_name='providers',
        blank=True,
    )

    @property
    def requires_npi(self):
        return self.title == 'MD'

    @property
    def requires_dea(self):
        return self.title == 'MD'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Credential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_number = models.CharField(max_length=100, blank=True, default='')
    last_checked_at = models.DateTimeField(null=True, blank=True)
    enumeration_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='credentials/', null=True, blank=True)

    class Meta:
        abstract = True


class NpiCredential(Credential):
    def __str__(self):
        return f'NPI {self.license_number}'


class DeaCredential(Credential):
    def __str__(self):
        return f'DEA {self.license_number}'


class ProviderByPractice(models.Model):
    class TypeChoices(models.TextChoices):
        DEFAULT = 'default', 'Default'
        MEDICAL_DIRECTOR = 'medical_director', 'Medical Director'

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='provider_practices',
    )
    practice = models.ForeignKey(
        Practice,
        on_delete=models.CASCADE,
        related_name='provider_practices',
    )
    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        default=TypeChoices.DEFAULT,
    )

    class Meta:
        unique_together = [('provider', 'practice')]

    def __str__(self):
        return f'{self.provider} — {self.practice} ({self.type})'
