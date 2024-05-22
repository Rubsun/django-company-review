from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from uuid import uuid4
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import re

def get_datetime() -> datetime:
    return datetime.now(timezone.utc)


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


def check_valid_phone(phone: str):
    pattern = r'^(\+\d{1,2})?(\d{3}[-\.\s]?\d{3}[-\.\s]?\d{4})$'
    if not re.match(pattern, phone):
        raise ValidationError(_('Invalid phone number format!'))


def check_modified(dt: datetime) -> None:
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'modified': dt}
        )


def check_created(dt: datetime) -> None:
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'created': dt}
        )


class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'), null=True, blank=True,
        default=get_datetime, validators=[check_created],
    )

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'), null=True, blank=True,
        default=get_datetime, validators=[check_modified],
    )

    class Meta:
        abstract = True


class Company(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False)
    phone = models.TextField(_('phone'), null=False, blank=False, validators=[check_valid_phone])
    address = models.TextField(_('address'), null=False, blank=False)

    equipments = models.ManyToManyField('Equipment', verbose_name=_('equipments'), through='CompanyEquipment')

    def __str__(self):
        return f'{self.title}: {self.phone}, {self.address}'

    class Meta:
        db_table = '"companies_schema"."company"'
        ordering = ['title', 'phone', 'address']
        verbose_name = _('company')
        verbose_name_plural = _('companies')

class Category(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = '"companies_schema"."category"'
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Equipment(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False)
    size = models.IntegerField(_('size'), null=True, blank=True, validators=[MinValueValidator(0)])
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('category'), related_name='equipments')
    companies = models.ManyToManyField('Company', verbose_name=_('companies'), through='CompanyEquipment')

    def __str__(self):
        return f'{self.category}: {self.title}, {self.size}'

    class Meta:
        db_table = '"companies_schema"."equipment"'
        ordering = ['title', 'size']
        verbose_name = _('equipment')
        verbose_name_plural = _('equipment')

    def get_reviews(self):
        return self.review_set.all()


class Review(UUIDMixin, CreatedMixin, ModifiedMixin):
    text = models.TextField(_('text'), null=False, blank=False)
    rating = models.PositiveIntegerField(
        _('grade'),
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=False,
        blank=False)

    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False, blank=False)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, null=False, blank=False, related_name='reviews')

    def __str__(self):
        return f'{self.text}: {self.rating}'

    class Meta:
        db_table = '"companies_schema"."review"'
        verbose_name_plural = _('reviews')
        verbose_name = _('reviews')
        ordering = ['text', 'rating']


class CompanyEquipment(UUIDMixin, CreatedMixin):
    company = models.ForeignKey(Company, verbose_name=_('company'), on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, verbose_name=_('equipment'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company} - {self.equipment}'

    class Meta:
        db_table = '"companies_schema"."company_equipment"'
        unique_together = (('company', 'equipment'),)
        verbose_name = _('relation Company Equipment')
        verbose_name_plural = _('relation Company Equipment')


class Client(UUIDMixin, ModifiedMixin, CreatedMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def first_name(self) -> str:
        return self.user.first_name

    @property
    def last_name(self) -> str:
        return self.user.last_name

    @property
    def email(self) -> str:
        return self.user.email

    def __str__(self) -> str:
        return f'{self.username} {self.first_name} {self.last_name}'

    class Meta:
        db_table = '"companies_schema"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('client')




