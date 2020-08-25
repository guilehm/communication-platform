import uuid

from django.db import models
from django.core.exceptions import ValidationError


class Addressee(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, blank=True, null=True)
    device_token = models.CharField(max_length=255, null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Addressee #{self.id} ({self.name or ""})'


class Scheduling(models.Model):
    TYPE_EMAIL = 'email'
    TYPE_SMS = 'sms'
    TYPE_PUSH = 'push'
    TYPE_WHATSAPP = 'whatsapp'
    TYPE_CHOICES = (
        (TYPE_EMAIL, 'Email'),
        (TYPE_SMS, 'SMS'),
        (TYPE_PUSH, 'Push'),
        (TYPE_WHATSAPP, 'WhatsApp'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    addressee = models.ForeignKey(
        'core.Addressee',
        related_name='schedules',
        on_delete=models.CASCADE,
    )
    message = models.TextField()
    sending_time = models.DateTimeField(db_index=True)
    type = models.CharField(
        max_length=64,
        choices=TYPE_CHOICES,
        db_index=True,
    )
    sent = models.BooleanField(default=False, db_index=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'schedules'

    def __str__(self):
        return f'Scheduling #{self.id} ({self.type}) ({self.addressee.name or ""})'

    def _validate_type(self):
        error_message = 'Addressee {information} is required for this communication type'
        if self.type in (self.TYPE_SMS, self.TYPE_WHATSAPP) and not self.addressee.mobile_number:
            raise ValidationError(error_message.format(information='mobile number'))
        elif self.type == self.TYPE_PUSH and not self.addressee.device_token:
            raise ValidationError(error_message.format(information='device token'))
        elif self.type == self.TYPE_EMAIL and not self.addressee.email:
            raise ValidationError(error_message.format(information='email'))

    def save(self, *args, **kwargs):
        self._validate_type()
        super().save(*args, **kwargs)
