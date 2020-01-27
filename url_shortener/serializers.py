import datetime
import re
import string
import random

from rest_framework import serializers

from .models import Url

URL_REGEXP = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
IP_REGEXP = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
SHORTENED_URL_REGEXP = r'[A-z0-9]{1,6}'


class UrlSerializer(serializers.Serializer):
    full_url = serializers.CharField(max_length=255)
    shortened_url = serializers.CharField(max_length=6, allow_null=True)

    creator_ip = serializers.CharField(max_length=15)  # ipv6?
    counter = serializers.IntegerField(default=0)
    last_redirect_datetime = serializers.DateTimeField(allow_null=True, default=None)

    def validate(self, data):
        if not re.match(IP_REGEXP, data['creator_ip']):
            raise serializers.ValidationError('Wrong IP adress')

        if not re.match(URL_REGEXP, data['full_url']):
            raise serializers.ValidationError('Invalid URL, consider using http(s)://<name>.<domain>')

        if not re.match(SHORTENED_URL_REGEXP, data['shortened_url']):
            raise serializers.ValidationError('Wrong shortened url, consider using only A-z, 0-9, 1-6 symbols')

        return data

    def create(self, validated_data):
        return Url.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.full_url = validated_data.get('full_url', instance.full_url)
        instance.shortened_url = validated_data.get('shortened_url', instance.full_url)
        instance.save()

        return instance

    @staticmethod
    def counter_increment(instance):
        instance.counter += 1
        instance.last_redirect_datetime = datetime.datetime.now()

        instance.save()

        return instance

    @staticmethod
    def generate_shortened_url(max_length=6):
        return ''.join([random.choice(string.ascii_letters + string.digits) for x in range(max_length)])

