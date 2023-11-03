from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['creator', 'created_at']
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        if serializer.context['request'].user == self.request.user:
            serializer.save()
        else:
            print('Попытка подмены данных пользователя')

    def perform_update(self, serializer):
        if serializer.context['request'].user == self.request.user:
            serializer.save()
        else:
            print('Ошибка авторизации')

    def partial_update(self, request, *args, **kwargs):
        adv_temp = Advertisement.objects.get(pk=kwargs['pk'])
        user_temp = adv_temp.creator.username
        kwargs['partial'] = True
        if request.user.username == user_temp:
            return self.update(request, *args, **kwargs)
        else:
            print("Ошибка авторизации")
            return HttpResponse('Ошибка авторизации')

    def perform_destroy(self, instance):
        if self.request.auth.user.auth_token == instance.creator.auth_token:
            instance.delete()
        else:
            print("Ошибка авторизации")

