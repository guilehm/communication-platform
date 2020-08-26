import pytest
from django.core.exceptions import ValidationError

from communication.core.models import Scheduling


def schedule_creation_util(addressee, comm_type):
    return Scheduling.objects.create(
        addressee=addressee,
        message='Hello! Your book "The Fellowship of the Ring" just left for delivery!',
        sending_time='2020-09-25 22:00:00',
        type=comm_type,
        sent=False,
    )


@pytest.mark.django_db
class TestSchedulingCreationForEmailType:

    def test_scheduling_with_email_type_must_not_be_created_without_addressee_email(self, addressee_without_email):
        with pytest.raises(ValidationError):
            schedule_creation_util(addressee_without_email, Scheduling.TYPE_EMAIL)
        assert Scheduling.objects.exists() is False

    def test_scheduling_with_email_type_must_be_created_with_addressee_email(self, addressee_with_email):
        scheduling = schedule_creation_util(addressee_with_email, Scheduling.TYPE_EMAIL)
        assert Scheduling.objects.exists() is True
        assert scheduling.addressee.email == 'gandalf@gmail.com'
        assert scheduling.type == Scheduling.TYPE_EMAIL


@pytest.mark.django_db
class TestSchedulingCreationForSMSType:

    def test_scheduling_with_sms_type_must_not_be_created_without_addressee_mob_number(self, addressee_without_mobile):
        with pytest.raises(ValidationError):
            schedule_creation_util(addressee_without_mobile, Scheduling.TYPE_SMS)
        assert Scheduling.objects.exists() is False

    def test_scheduling_with_sms_type_must_be_created_with_addressee_mob_number(self, addressee_with_mobile):
        scheduling = schedule_creation_util(addressee_with_mobile, Scheduling.TYPE_SMS)
        assert Scheduling.objects.exists() is True
        assert scheduling.addressee.mobile_number == '+55 11 99445-9999'
        assert scheduling.type == Scheduling.TYPE_SMS


@pytest.mark.django_db
class TestSchedulingCreationForWhatsAppType:

    def test_scheduling_with_whatsapp_type_must_not_be_created_without_addressee_mob_number(
            self, addressee_without_mobile
    ):
        with pytest.raises(ValidationError):
            schedule_creation_util(addressee_without_mobile, Scheduling.TYPE_WHATSAPP)
        assert Scheduling.objects.exists() is False

    def test_scheduling_with_whatsapp_type_must_be_created_with_addressee_mob_number(self, addressee_with_mobile):
        scheduling = schedule_creation_util(addressee_with_mobile, Scheduling.TYPE_WHATSAPP)
        assert Scheduling.objects.exists() is True
        assert scheduling.addressee.mobile_number == '+55 11 99445-9999'
        assert scheduling.type == Scheduling.TYPE_WHATSAPP


@pytest.mark.django_db
class TestSchedulingCreationForPushType:

    def test_scheduling_with_push_type_must_not_be_created_without_addressee_device_token(
            self, addressee_without_device_token
    ):
        with pytest.raises(ValidationError):
            schedule_creation_util(addressee_without_device_token, Scheduling.TYPE_PUSH)
        assert Scheduling.objects.exists() is False

    def test_scheduling_with_push_type_must_be_created_with_addressee_device_token(self, addressee_with_device_token):
        scheduling = schedule_creation_util(addressee_with_device_token, Scheduling.TYPE_PUSH)
        assert Scheduling.objects.exists() is True
        assert scheduling.addressee.device_token == '740f4707 bebcf74f 9b7c25d4 8e335894'
        assert scheduling.type == Scheduling.TYPE_PUSH
