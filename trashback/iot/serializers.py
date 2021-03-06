from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Device, Goal
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import MeasurementDocument, DeviceDocument


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'owner', 'measurements')


class MeasurementSerializer(DocumentSerializer):
    class Meta:
        document = MeasurementDocument
        fields = ('id', 'device', 'value', 'key')


class DeviceSerializer(DocumentSerializer):
    class Meta:
        document = DeviceDocument
        fields = ('id', 'name', 'owner')


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'key', 'target', 'name', 'owner')


class UserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ('id', 'username', 'devices')
