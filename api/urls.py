from rest_framework import routers
from django.urls import path
from short.views import SitesVisitAPIListView, SitesVisitTodayAPIListView, URLShortCreateAPIView, TopThreeVisitAPIView, URLOnlyAPIListView 

app_name = 'api'

router = routers.DefaultRouter()
router.register('url-short', URLShortCreateAPIView)
router.register('url-only', URLOnlyAPIListView)
urlpatterns = [
    path('visited/', SitesVisitAPIListView.as_view(), name='visited'),
    path('sites-visit-today/', SitesVisitTodayAPIListView.as_view()),
    path('top-three-visits/', TopThreeVisitAPIView.as_view(), name='top_three')
] 

urlpatterns += router.urls



