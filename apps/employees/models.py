from django.core.validators import MinLengthValidator
from django.db import models

from apps.core.validators import phone_and_fax_number_validator


class Employee(models.Model):
    id = models.AutoField(
        db_column='EmployeeId',
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
    title = models.CharField(
        max_length=255,
        verbose_name='title',
        db_column='Title',
    )
    birthdate = models.DateTimeField(
        verbose_name='birth date',
        db_column='BirthDate',
        blank=True,
        null=True
    )
    hire_date = models.DateTimeField(
        verbose_name='hire date',
        db_column='HireDate',
    )
    address = models.CharField(
        max_length=255,
        verbose_name='address',
        db_column='Address',
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
    )
    phone = models.CharField(
        max_length=32,
        verbose_name='phone number',
        db_column='Phone',
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
        unique=True
    )

    reports_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='subordinates',
        verbose_name='reports to',
        db_column='ReportsTo',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'Employee'
        ordering = ['first_name', 'last_name']
        verbose_name = 'employee'
        verbose_name_plural = 'employees'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)
