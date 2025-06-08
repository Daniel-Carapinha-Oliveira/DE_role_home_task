from django.core.validators import MinValueValidator
from django.db import models


class Invoice(models.Model):
    id = models.AutoField(
        db_column='InvoiceId',
        primary_key=True
    )
    invoice_date = models.DateTimeField(
        verbose_name='birth date',
        db_column='InvoiceDate',
    )
    billing_address = models.CharField(
        max_length=255,
        verbose_name='billing address',
        db_column='BillingAddress',
        blank=True,
        null=True
    )
    billing_city = models.CharField(
        max_length=128,
        verbose_name='billing city',
        db_column='BillingCity',
        blank=True,
        null=True
    )
    billing_state = models.CharField(
        max_length=128,
        verbose_name='billing state',
        db_column='BillingState',
        blank=True,
        null=True
    )
    billing_country = models.CharField(
        max_length=64,
        verbose_name='billing country',
        db_column='BillingCountry',
        blank=True,
        null=True
    )
    billing_postal_code = models.CharField(
        max_length=20,
        verbose_name='billing postal code',
        db_column='BillingPostalCode',
        blank=True,
        null=True
    )
    total = models.DecimalField(
        verbose_name='total',
        db_column='Total',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        related_name='invoices',
        db_column='CustomerId',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'Invoice'
        ordering = ['-invoice_date', ]
        verbose_name = 'invoice'
        verbose_name_plural = 'invoices'

    def __str__(self):
        return self.invoice_date.strftime('%Y-%m-%d %H:%M:%S')

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)


class InvoiceLine(models.Model):
    id = models.AutoField(
        db_column='InvoiceLineId',
        primary_key=True
    )
    unit_price = models.DecimalField(
        verbose_name='price',
        db_column='UnitPrice',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    quantity = models.PositiveIntegerField(
        verbose_name='quantity',
        db_column='Quantity'
    )

    invoice = models.ForeignKey(
        'sales.Invoice',
        on_delete=models.PROTECT,
        related_name='invoice_lines',
        db_column='InvoiceId'
    )
    track = models.ForeignKey(
        'music.Track',
        on_delete=models.PROTECT,
        related_name='invoice_lines',
        db_column='TrackId'
    )

    class Meta:
        db_table = 'InvoiceLine'
        ordering = ['id']
        verbose_name = 'invoice line'
        verbose_name_plural = 'invoice lines'

    def __str__(self):
        return f'{self.invoice} - {self.track}'

    def save(self, *args, **kwargs):
        # Run Django model validation (max_length, blank, custom validators, etc.).
        # This is especially needed on SQLite, which doesn’t enforce max_length or
        # other field constraints at the database level.
        self.full_clean()
        super().save(*args, **kwargs)
