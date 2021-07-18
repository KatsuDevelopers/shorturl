import re
import string
import random
from django.conf import settings
from rest_framework import serializers
from .models import DateVisited, URL, URLVisit

class URLTotalCountSerializer(serializers.ModelSerializer):
    url_name = serializers.CharField(write_only=True, allow_blank=True)
    auto = serializers.BooleanField(write_only=True)
    alias = serializers.URLField(read_only=True)
    total_count = serializers.SerializerMethodField()
    class Meta:
        model = URL
        fields = ['alias', 'original', 'total_count', 'url_name', 'auto']

    def get_total_count(self, instance):
        return instance.total_count()

    def create(self, validated_data):
        if validated_data['auto'] == True:
            validated_data['alias'] = self.auto_generate()
        else:
            self.check_length(validated_data['url_name'])
            validated_data['alias'] = f'http://{settings.HOST_ADDRESS}/{validated_data["url_name"]}'
        del validated_data['auto']
        del validated_data['url_name'] 
        url = super().create(validated_data)
        return url

    def auto_generate(self):
        letter_digits = string.ascii_letters + string.digits
        uri = ''.join(random.choice(letter_digits) for i in range(5))
        return f'http://{settings.HOST_ADDRESS}/{uri}'
    
    def check_length(self, uri:str):
        if len(uri) != 5:
            raise serializers.ValidationError('alias is not 5 letters long')

    # def create(self, validated_data):
    #     validated_data['alias'] = self.url_edited(validated_data['url_name'])
    #     del validated_data['url_name']
    #     url = super().create(validated_data)
    #     return url

    # def url_edited(self, url:str):
    #     url = re.sub('[^A-Za-z0-9]+', '-', url)
    #     if len(url.split("-")) > 5 or len(url.split("-")) == 1:
    #         raise serializers.ValidationError("URI\'s is incorrect please enter between 2 to 5 words" )
    #     url = f'http://{settings.HOST_ADDRESS}/{url}'
    #     if not URL.objects.filter(alias=url):
    #         return url
    #     else:
    #         raise serializers.ValidationError('alias exists, please choose another name')

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        exclude = ['id']
class URLOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['alias']

class SiteVisitListSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    class Meta:
        model = DateVisited
        fields = ['date_visited', 'value']

    def get_value(self, instance):
        date_visit = DateVisited.objects.filter(date_visited=instance.date_visited)
        date_visit_id = date_visit.values_list('id', flat=True)
        url_visit = URLVisit.objects.filter(id__in=date_visit_id)
        data = list()
        for url in date_visit:
            temp_dict = {
                'alias': url.url.alias,
                'original': url.url.original,
                'count': url_visit.get(date_url_visited=url, url=url.url.id).count
            }
            data.append(temp_dict)
        return data
            
class SiteVisitSerializer(SiteVisitListSerializer):
    value = serializers.SerializerMethodField()