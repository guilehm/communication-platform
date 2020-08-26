from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from communication.core.models import Addressee, Scheduling


class AddresseeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    mobileNumber = serializers.CharField(source='mobile_number', required=False)
    deviceToken = serializers.CharField(source='device_token', required=False)

    class Meta:
        model = Addressee
        fields = (
            'id',
            'name',
            'email',
            'mobileNumber',
            'deviceToken',
        )


class SchedulingUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scheduling
        fields = (
            'sent',
        )


class SchedulingSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    sendingTime = serializers.DateTimeField(source='sending_time')
    addressee = AddresseeSerializer()

    dateAdded = serializers.CharField(source='date_added', read_only=True)
    dateChanged = serializers.CharField(source='date_changed', read_only=True)

    class Meta:
        model = Scheduling
        fields = (
            'id',
            'addressee',
            'message',
            'sendingTime',
            'type',
            'sent',
            'dateAdded',
            'dateChanged',
        )

    @staticmethod
    def validate_addressee(data):
        addressee_id = data.get('id')
        if addressee_id is not None:
            if any(map(lambda x: x in data, ['name', 'email', 'mobile_number', 'device_token'])):
                raise serializers.ValidationError({
                    'error': 'To use an existing Addressee you must fill only id.'
                })
            try:
                Addressee.objects.get(id=addressee_id)
            except Addressee.DoesNotExist:
                raise serializers.ValidationError({
                    'error': f'Addressee with id {addressee_id} does not exist.'
                })
        return data

    def create(self, validated_data):
        addressee_data = validated_data.pop('addressee')
        with transaction.atomic():
            addressee, created = Addressee.objects.get_or_create(
                id=addressee_data.pop('id', None),
                defaults=addressee_data,
            )
            try:
                return Scheduling.objects.create(
                    addressee=addressee,
                    **validated_data,
                )
            except ValidationError as exc:
                raise serializers.ValidationError({
                    'error': exc.message,
                })
