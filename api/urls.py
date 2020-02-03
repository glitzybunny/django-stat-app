from django.conf.urls import url, include
from api import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^users$', views.AllUsersView.as_view(), name='users'),

    url(r'^users/(?P<id>[0-9]+)/$', views.UserView.as_view(), name='user'),
]