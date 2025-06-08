from django.db import models
from django.core.validators import MinLengthValidator

from apps.core.validators import phone_and_fax_number_validator


class Customer(models.Model):
    id = models.AutoField(
        db_column='CustomerId',
        primary_key=True
    )
    first_name = models.CharField(
        max_length=64,
        verbose_name='first name',
        db_column='FirstName'
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name='last name',
        db_column='LastName'
    )
    company = models.CharField(
        max_length=128,
        verbose_name='company',
        db_column='Company',
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=255,
        verbose_name='address',
        db_column='Address',
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=128,
        verbose_name='city',
        db_column='City',
    )
    state = models.CharField(
        max_length=128,
        verbose_name='state',
        db_column='State',
    )
    country = models.CharField(
        max_length=64,
        verbose_name='country',
        db_column='Country',
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name='postal code',
        db_column='PostalCode',
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=32,
        verbose_name='phone number',
        db_column='Phone',
        blank=True,
        null=True,
        unique=True,
        validators=[
            phone_and_fax_number_validator,
            MinLengthValidator(6, message='Phone number must be at least 6 characters long.')
        ]
    )
    fax = models.CharField(
        max_length=32,
        verbose_name='fax',
        db_column='Fax',
        blank=True,
        null=True,
        validators=[
            phone_and_fax_number_validator,
            MinLengthValidator(6, message='Phone number must be at least 6 characters long.')
        ]
    )
    email = models.EmailField(
        verbose_name='email',
        db_column='Email',
        unique=True,
        blank=True,
        null=True,
    )
    support_representative = models.ForeignKey(
        'employees.Employee',
        on_delete=models.PROTECT,
        related_name='customers',
        verbose_name='support representative',
        db_column='SupportRepId',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'Customer'
        ordering = ['first_name', 'last_name']
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)
