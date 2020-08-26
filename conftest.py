import pytest

from communication.core.models import Addressee, Scheduling


@pytest.fixture
def addressee():
    return Addressee.objects.create(
        name='Frodo Baggings',
        email='frodo@gmail.com',
        mobile_number='+55 16 99999-4455',
        device_token='740f4707 bebcf74f 9b7c25d4 8e335894',
    )


@pytest.fixture
def addressee_without_email():
    return Addressee.objects.create(
        name='Gandalf the Grey',
        email=None,
    )


@pytest.fixture
def addressee_with_email():
    return Addressee.objects.create(
        name='Gandalf the Grey',
        email='gandalf@gmail.com',
    )


@pytest.fixture
def addressee_without_mobile():
    return Addressee.objects.create(
        name='Legolas the Elf',
        mobile_number=None,
    )


@pytest.fixture
def addressee_with_mobile():
    return Addressee.objects.create(
        name='Legolas the Elf',
        mobile_number='+55 11 99445-9999',
    )


@pytest.fixture
def addressee_without_device_token():
    return Addressee.objects.create(
        name='Boromir',
        device_token=None,
    )


@pytest.fixture
def addressee_with_device_token():
    return Addressee.objects.create(
        name='Boromir',
        device_token='740f4707 bebcf74f 9b7c25d4 8e335894',
    )


@pytest.fixture
def scheduling(addressee):
    return Scheduling.objects.create(
        addressee=addressee,
        message='Hello! Your book "The Fellowship of the Ring" just left for delivery!',
        sending_time='2020-09-25T22:00:00Z',
        type='sms',
        sent=False,
    )
