from django.urls import path
from . import views

app_name='short_url'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('or/list_url/', views.URLListView.as_view(), name='index'),
    path('or/top_three/', views.TopThreeSitesView.as_view(), name='top_three'),
    path('or/visited/', views.SitesVisitListView.as_view(), name='visited'),
    path('or/create/', views.create_url, name='create'),
    path('or/alias_list', views.URLOnlyListView.as_view(), name='alias_list'),
    path('<str:uri>/', views.redirect_url)
]
