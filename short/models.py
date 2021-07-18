from django.db import models
from django.db.models import F, Q, Sum, Count
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, timedelta


class URLQuerySet(models.QuerySet):

    def top_three_visit(self):
        return self.annotate(count=Sum('url_visit__count')).filter(count__gt=0).order_by('-count')[:3]
    
class URLTopManager(models.Manager):
    def get_queryset(self):
        return URLQuerySet(self.model, using=self._db)
    
    
    def top_three_visit(self):
        return self.get_queryset().top_three_visit()

class URL(models.Model):
    alias = models.URLField(unique=True, max_length=500)
    original = models.URLField(max_length=500)

    def total_count(self):
        count = int()
        url_visits = self.url_visit.all()
        for day in url_visits:
            count += day.count
        return count
    
    def add_visit_count(self):
        url_visit_last = self.url_date.last()
        if not url_visit_last or url_visit_last.date_visited != date.today():
            date_visit = DateVisited.objects.create(url=self)
            url_visit_last = URLVisit.objects.create(url=self, date_url_visited=date_visit, count=1)
        else:
            URLVisit.objects.get(url=self, date_url_visited=url_visit_last).increment_count()
    
    def todays_visit(self):
        try:
            today_url_visit = self.url_date.get(date=date.today())
        except ObjectDoesNotExist:
            return None
        return today_url_visit

    
    objects = models.Manager()
    top = URLTopManager() 

class DateVisitQuery(models.QuerySet):

    def sites_visit_today(self):
        return self.filter(Q(date_visited=date.today()) & Q(date_visit__count__gt=0))

    def ids_count_gt_one(self, day):
        return self.filter(Q(date_visited=day) & Q(date_visit__count__gt=0))

class DateVisitManager(models.Manager):
    def get_queryset(self):
        return DateVisitQuery(self.model, self._db)
    
    def sites_visit_today(self):
        return self.get_queryset().sites_visit_today()
    
    def id_count_gt_one(self, day):
        return self.get_queryset().ids_count_gt_one(day)

class DateVisited(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='url_date')
    date_visited = models.DateField(auto_now_add=True)

    objects = models.Manager()
    visit = DateVisitManager()

class URLVisit(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='url_visit')
    count = models.PositiveIntegerField(default=0)
    date_url_visited = models.ForeignKey(DateVisited, on_delete=models.CASCADE, related_name='date_visit')

    def increment_count(self):
        self.count = F('count') + 1
        self.save()
    
    objects = models.Manager()