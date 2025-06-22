from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from num2words import num2words


class Person(models.Model):
    GENDER_CHOICES = [('M', 'Мужской'), ('F', 'Женский')]

    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    passport_series = models.CharField(
        max_length=4,
        validators=[MinLengthValidator(4)],
        verbose_name="Серия паспорта"
    )
    passport_number = models.CharField(
        max_length=6,
        validators=[MinLengthValidator(6)],
        verbose_name="Номер паспорта"
    )
    issued_by = models.TextField(verbose_name="Кем выдан")
    registration = models.TextField(verbose_name="Адрес регистрации")

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_name or "Новая персона"


class Seller(Person):
    is_individual = models.BooleanField(default=True, verbose_name="Физ. лицо")

    def __str__(self):
        return f"Продавец: {super().__str__()}"


class Buyer(Person):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    def __str__(self):
        return f"Покупатель: {super().__str__()}"


class RealEstate(models.Model):
    PROPERTY_TYPES = [
        ('LAND', 'Земельный участок'),
        ('APARTMENT', 'Квартира'),
        ('HOUSE', 'Дом с участком')
    ]

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    cadastral_number = models.CharField(max_length=30)
    address = models.TextField()
    area = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        prop_type = dict(self.PROPERTY_TYPES).get(self.property_type, 'Неизвестный тип')
        return f"{prop_type} ({self.address})"


class DKPTemplate(models.Model):
    DOC_TYPES = [
        ('LAND', 'Земельный участок'),
        ('APARTMENT', 'Квартира'),
        ('HOUSE', 'Дом с участком')
    ]
    name = models.CharField(max_length=100)
    template_file = models.FileField(upload_to='templates/')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)

    def __str__(self):
        return self.name


class GeneratedDKP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(DKPTemplate, on_delete=models.PROTECT)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_in_words = models.CharField(max_length=200, blank=True)
    document = models.FileField(upload_to='generated_docs/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.price_in_words:
            self.price_in_words = num2words(int(self.price), lang='ru') + ' рублей'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ДКП ({self.real_estate})"