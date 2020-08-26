import pytest
from django.urls import reverse
from rest_framework import status

from communication.core.models import Addressee, Scheduling


@pytest.mark.django_db
class TestSchedulingViews:

    @pytest.fixture
    def scheduling_response(self, scheduling):
        return {
            'id': str(scheduling.id),
            'addressee': {
                'id': scheduling.addressee.id,
                'name': scheduling.addressee.name,
                'email': scheduling.addressee.email,
                'mobileNumber': scheduling.addressee.mobile_number,
                'deviceToken': scheduling.addressee.device_token,
            },
            'message': scheduling.message,
            'sendingTime': str(scheduling.sending_time),
            'type': scheduling.type,
            'sent': scheduling.sent,
            'dateAdded': str(scheduling.date_added),
            'dateChanged': str(scheduling.date_changed),
        }

    @pytest.fixture
    def scheduling_post_data(self):
        return {
            "addressee": {
                "name": "Bilbo Baggins",
                "email": "bilbo@gmail.com",
                "mobileNumber": "+55 11 99988-9080",
                "deviceToken": "8e335894 9b7c25d4 bebcf74f 740f4707"
            },
            "message": "Bilbo has always been frustrated with several of the more famous tales of Elvish history",
            "sendingTime": "2020-08-30T02:05:00.472Z",
            "type": "email",
            "sent": False
        }

    @pytest.fixture
    def scheduling_post_data_for_existing_addressee(self, addressee):
        return {
            "addressee": {"id": addressee.id},
            "message": "Bilbo does not know this but part of the reason why "
                       "Lobelia Sackville-Baggins nee Bracegirdle was so keen to have Bag End was "
                       "because she’d always wanted to marry Bilbo instead of his cousin Otho",
            "sendingTime": "2020-08-30T02:05:00.472Z",
            "type": "email",
            "sent": False
        }

    @pytest.fixture
    def invalid_scheduling_post_data(self, addressee):
        return {
            "addressee": {
                "id": addressee.id,
                "name": "Frodo Baggins"
            },
            "message": "Bilbo was not an ordinary hobbit. His mother was Belladona Took, "
                       "and they say that Tooks look 'fairy' as if they had elven blood in them",
            "sendingTime": "2020-08-30T02:05:00.472Z",
            "type": "email",
            "sent": False
        }

    def test_scheduling_read_response(self, client, scheduling, scheduling_response):
        url = reverse('scheduling-detail', kwargs={'pk': scheduling.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == scheduling_response

    def test_should_update_scheduling_status_in_patch_endpoint(self, client, scheduling):
        url = reverse('scheduling-detail', kwargs={'pk': scheduling.id})
        instance = Scheduling.objects.get(id=scheduling.id)
        assert instance.sent is False
        response = client.patch(url, data={'sent': "true"}, content_type='application/json')
        instance.refresh_from_db()
        assert instance.sent is True
        assert response.status_code == status.HTTP_200_OK

    def test_should_delete_scheduling_in_delete_endpoint(self, client, scheduling):
        url = reverse('scheduling-detail', kwargs={'pk': scheduling.id})
        assert Scheduling.objects.exists() is True
        response = client.delete(url)
        assert Scheduling.objects.exists() is False
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_create_scheduling_and_addressee(self, client, scheduling_post_data):
        url = reverse('scheduling-list')
        assert Scheduling.objects.exists() is False
        assert Addressee.objects.exists() is False
        response = client.post(url, data=scheduling_post_data, content_type='application/json')
        assert Scheduling.objects.exists() is True
        assert Addressee.objects.exists() is True
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_create_scheduling_for_an_existing_addressee(
            self, client, addressee, scheduling_post_data_for_existing_addressee
    ):
        url = reverse('scheduling-list')
        assert Scheduling.objects.exists() is False
        assert Addressee.objects.exists() is True
        response = client.post(url, data=scheduling_post_data_for_existing_addressee, content_type='application/json')
        assert Scheduling.objects.exists() is True
        assert response.status_code == status.HTTP_201_CREATED
        addressee = Addressee.objects.get(id=addressee.id)
        scheduling = Scheduling.objects.get(id=response.json()['id'])
        assert scheduling.addressee.id is addressee.id

    def test_should_not_accept_id_and_addressee_data(self, client, invalid_scheduling_post_data):
        url = reverse('scheduling-list')
        assert Scheduling.objects.exists() is False
        response = client.post(url, data=invalid_scheduling_post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Scheduling.objects.exists() is False

    def test_patch_endpoint_should_not_update_fields_other_than_sent_status(self, client, scheduling):
        url = reverse('scheduling-detail', kwargs={'pk': scheduling.id})
        instance = Scheduling.objects.get(id=scheduling.id)
        assert instance.type == Scheduling.TYPE_SMS
        assert instance.sent is False
        response = client.patch(
            url, data={'type': Scheduling.TYPE_PUSH, 'sent': True}, content_type='application/json'
        )
        instance.refresh_from_db()
        assert instance.type == Scheduling.TYPE_SMS
        assert instance.type != Scheduling.TYPE_PUSH
        assert instance.sent is True
        assert response.status_code == status.HTTP_200_OK
