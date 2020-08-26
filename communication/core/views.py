from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from communication.core.models import Scheduling
from communication.core.serializers import SchedulingSerializer, SchedulingUpdateSerializer


class SchedulingViewSet(RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Scheduling.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if 'update' in self.action:
            return SchedulingUpdateSerializer
        return SchedulingSerializer
