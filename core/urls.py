from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^$', views.indexView.as_view(), name='index'),
    url(r'^users/(?P<id>[0-9]+)/$',
        views.userProfileView.as_view(), name='user'),

    url(r'^get_chart_data/$', views.get_chart_data),

]
