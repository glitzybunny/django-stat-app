from rest_framework import routers, serializers, viewsets

from django.contrib.auth.models import User, Group
from core import models


class UserSerializer(serializers.ModelSerializer):
    total_clicks = serializers.ReadOnlyField()
    total_page_views = serializers.ReadOnlyField()

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'gender', 'ip_address', 'total_clicks', 'total_page_views')
