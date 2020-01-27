import copy

from django.shortcuts import redirect
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Url
from .serializers import UrlSerializer


class UrlView(APIView):
    def get(self, request, short_id):

        url = get_object_or_404(Url.objects.all(), shortened_url=short_id)
        serializer = UrlSerializer(url, many=False)

        if request.META.get('REMOTE_ADDR') != serializer.data.get('creator_ip'):
            hidden_values_dict = copy.deepcopy(serializer.data)
            hidden_values_dict.update({'creator_ip': 'Not you', 'counter': 'Mind your own business'})
            return Response({'url': hidden_values_dict})
        return Response({'url': serializer.data})

    def put(self, request, short_id):
        url = get_object_or_404(Url.objects.all(), shortened_url=short_id)
        url_data = request.data.get('url')

        serializer = UrlSerializer(instance=url, data=url_data, partial=True)

        if request.META.get('REMOTE_ADDR') != url.creator_ip:
            return Response({'response': f'Only owner can update /{short_id}/'})

        if serializer.is_valid(raise_exception=True):
            url_updated = serializer.save()

        return Response({'response': f'URL {url_updated} uodated successfully'})

    def delete(self, request, short_id):
        url = get_object_or_404(Url.objects.all(), shortened_url=short_id)
        serializer = UrlSerializer(url, many=False)

        if request.META.get('REMOTE_ADDR') == url.creator_ip:
            url.delete()
            return Response({'response': f'/{short_id}/ deleted successfully'})
        return Response({'response': f'Only owner can delete /{short_id}/'}, status=204)


class UrlListView(APIView):
    permission_classes = ()
    authentication_classes = ()  # removing CSRF

    def get(self, request):
        urls = Url.objects.all()
        serializer = UrlSerializer(urls, many=True)

        for url in serializer.data:
            if request.META.get('REMOTE_ADDR') != url.get('creator_ip'):
                url.update({'creator_ip': 'Not you', 'counter': 'Mind your own business'})

        return Response({'urls': serializer.data})

    def post(self, request):
        url_data = request.data.get('url')
        creator_ip = request.META.get('REMOTE_ADDR')
        url_data.update({'creator_ip': creator_ip})
        if 'shortened_url' not in url_data.keys():  # random if not passed
            url_data.update({'shortened_url': UrlSerializer.generate_shortened_url()})

        serializer = UrlSerializer(data=url_data)

        if serializer.is_valid(raise_exception=True):
            url_saved = serializer.save()

        return Response({'response': f'Url {url_saved} created successfully'})


class RedirectView(APIView):
    def get(self, request, short_id):
        url = Url.objects.get(shortened_url=short_id)
        UrlSerializer.counter_increment(url)

        return redirect(url.full_url)
