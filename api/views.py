from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.conf import settings
from django.shortcuts import render
from core import models
from api import serializers


class AllUsersView(APIView):
    """
    API endpoint that retrieve Users data. (GET only)
    It has pagination(50 objects/page). 
    Send GET param 'page' equals to page num to go through pages.
    """

    def get(self, *args, **kwargs):
        queryset = models.User.objects.all()

        paginator = Paginator(
            queryset, settings.REST_FRAMEWORK.get('PAGE_SIZE'))
        page = self.request.GET.get('page')

        try:
            queryset = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            return Response(data={})

        serializer = serializers.UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserView(APIView):
    """
    API endpoint that retrieve User data. (GET only)
    """

    def get(self, *args, **kwargs):

        uid = self.kwargs.get('id')

        try:
            user_object = models.User.objects.get(id=uid)
            serializer = serializers.UserSerializer(user_object)

            return Response(serializer.data)

        except ObjectDoesNotExist:
            return Response(data={'message': 'Object does not exist!'})
