from datetime import datetime

from django.utils.timezone import utc
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from reversion.models import Version

from sapl.api.sessao.serializers import SessaoPlenariaOldSerializer,\
    SessaoPlenariaSerializer
from sapl.sessao.models import SessaoPlenaria


class SessaoPlenariaOldViewSet(ReadOnlyModelViewSet):

    permission_classes = (AllowAny,)
    serializer_class = SessaoPlenariaOldSerializer
    queryset = SessaoPlenaria.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('data_inicio', 'data_fim', 'interativa')


class SessaoPlenariaViewSet(ReadOnlyModelViewSet):

    permission_classes = (AllowAny,)
    serializer_class = SessaoPlenariaSerializer
    queryset = SessaoPlenaria.objects.all().order_by(
        '-data_inicio', '-hora_inicio')

    def get_queryset(self):
        qs = super().get_queryset()

        data = self.request.query_params.get('data', None)
        if data:
            data = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f')
            data = data.replace(tzinfo=utc)
            opts = SessaoPlenaria._meta
            vs = Version.objects.filter(
                revision__date_created__gte=data,
                content_type__app_label=opts.app_label,
                content_type__model=opts.model_name
            ).order_by(
                '-revision__date_created', '-object_id'
            ).values_list('object_id', flat=True)
            vs = set(vs)

            qs = qs.filter(id__in=vs)

        return qs
