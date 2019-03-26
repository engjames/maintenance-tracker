from django.shortcuts import render
from maintainance_requests.models import MaintainanceRequest
from maintainance_requests.serializers import MaintainanceRequestSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from django.http import JsonResponse
import logging

class MaintainanceRequestViewSet(ModelViewSet):
    """API Endpoint for viewing and editting user details"""
    queryset = MaintainanceRequest.objects.all().order_by('-date_posted')
    serializer_class = MaintainanceRequestSerializer

    filter_backends = (SearchFilter,)
    search_fields = ('request_title', 'request_description', 'author__username')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.is_superuser and "status" in self.request.data:
            serializer.save()
        elif "status" in self.request.data and not self.request.user.is_superuser:
            return Response("Unauthorized", status.HTTP_401_UNAUTHORIZED)

    def perform_update(self, serializer):
        logger = logging.getLogger(__name__)
        logger.error("The message")
        # if self.request.user.is_superuser:
        #     if "status" in self.request.data:
        #         serializer.save()
        #     return JsonResponse({"Missing some fields":"jfjjfjfkjfjdfkj"})
        # return JsonResponse({"You are not authorized": "jjjjjjdjdjdjdjdjd"})

    def list(self, request):
        if request.user.is_superuser:
            queryset = MaintainanceRequest.objects.all()
        else:
            user = request.user
            queryset = MaintainanceRequest.objects.filter(author=user)
        serializer = MaintainanceRequestSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)
        
