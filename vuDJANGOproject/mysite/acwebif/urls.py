from django.conf.urls import url

from . import views

app_name = 'acwebif'
urlpatterns = [
    url(r'^$',views.IndexView.as_view(), name='index'),
    url(r'^time/$', views.current_datetime, name='time'),
]
