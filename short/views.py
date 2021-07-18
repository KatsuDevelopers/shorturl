from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from .models import DateVisited, URL, URLVisit
from .serializer import SiteVisitSerializer, URLTotalCountSerializer, SiteVisitListSerializer, URLOnlySerializer

class URLShortCreateAPIView(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLTotalCountSerializer

class URLOnlyAPIListView(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLOnlySerializer

class SitesVisitTodayAPIListView(generics.ListAPIView):
    queryset = DateVisited.visit.sites_visit_today().distinct('date_visited')
    serializer_class = SiteVisitSerializer

class TopThreeVisitAPIView(generics.ListAPIView):
    queryset = URL.top.top_three_visit()
    serializer_class = URLTotalCountSerializer

class SitesVisitAPIListView(generics.ListAPIView):
    queryset = DateVisited.objects.filter(date_visit__count__gt=0).distinct('date_visited')
    serializer_class = SiteVisitListSerializer

def redirect_url(request:HttpRequest, uri:str):
    if request.method == 'GET':
        url_search_string = f'http://{settings.HOST_ADDRESS}/{uri}'
        try:
            url = URL.objects.get(alias=url_search_string)
        except ObjectDoesNotExist:
            return HttpResponse('Does not exist')
        url.add_visit_count()
        return HttpResponseRedirect(url.original)

def create_url(request:HttpRequest):
    return render(request, 'short/create.html')
        
class HomePage(TemplateView):
    template_name = "index.html"

class URLListView(ListView):
    model = URL
    template_name = 'short/index.html'
    context_object_name = 'URLS'

class TopThreeSitesView(ListView):
    queryset = URL.top.top_three_visit()
    template_name = 'short/top_three.html'
    context_object_name = 'URLS'

class SitesVisitListView(TemplateView):
    template_name = 'short/site_visit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sites"] = self.get_sites()
        return context

    def get_sites(self):
        data = list()
        q = DateVisited.objects.filter(date_visit__count__gt=0).distinct('date_visited')
        for date in q:
            ids = DateVisited.visit.id_count_gt_one(date.date_visited).values_list('id', flat=True)
            url_visit = URLVisit.objects.filter(date_url_visited__in=ids)
            for url in url_visit.order_by('-count'):
                temp_dict = {
                    'alias': url.url.alias,
                    'original': url.url.original,
                    'count': url.count
                }
                data.append(temp_dict)
        return data

class URLOnlyListView(ListView):
    queryset = URL.objects.all()
    template_name = 'short/alias_list.html'
    context_object_name = 'URLS'