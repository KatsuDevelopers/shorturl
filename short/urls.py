from django.urls import path
from . import views

app_name='short_url'

urlpatterns = [
    path('r/list_url/', views.URLListView.as_view(), name='index'),
    path('r/top_three/', views.TopThreeSitesView.as_view(), name='top_three'),
    path('r/visited/', views.SitesVisitListView.as_view(), name='visited'),
    path('r/create/', views.create_url, name='create'),
    path('r/alias_list', views.URLOnlyListView.as_view(), name='alias_list'),
    path('<str:uri>/', views.redirect_url),
    path('', views.HomePage.as_view(), name='home'),
]
