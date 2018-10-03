from collections import OrderedDict
from datetime import datetime

from django.db.models import Q
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
    deletados = None

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        response.data['deleted'] = self.deletados if self.deletados else []

        return response

    def get_queryset(self):
        qs = super().get_queryset()
        opts = SessaoPlenaria._meta

        data_min = self.request.query_params.get('data_min', None)
        data_max = self.request.query_params.get('data_max', None)
        tipo_update = self.request.query_params.get('tipo_update', '1')

        if data_min:
            data_min = datetime.strptime(data_min, '%Y-%m-%dT%H:%M:%S.%f')
            data_min = data_min.replace(tzinfo=utc)
        if data_max:
            data_max = datetime.strptime(data_max, '%Y-%m-%dT%H:%M:%S.%f')
            data_max = data_max.replace(tzinfo=utc)

        if data_min or data_max:
            if tipo_update == 'sync':
                q_model = Q(content_type__app_label=opts.app_label,
                            content_type__model=opts.model_name)

                q_data = Q()
                if data_min:
                    q_data &= Q(revision__date_created__gte=data_min)

                if data_max:
                    q_data &= Q(revision__date_created__lte=data_max)

                vs = Version.objects.filter(q_model).order_by(
                    '-revision__date_created', '-object_id')

                vs_sync = vs.filter(q_data).values_list('object_id', flat=True)
                vs_sync = set(map(int, vs_sync))

                # com o código abaixo envia todos os deletados no período sel.
                qs = qs.filter(id__in=vs_sync)
                qs_values = set(qs.values_list('id', flat=True))
                self.deletados = vs_sync - qs_values

                # com código abaixo envia todos os deletados
                # qs_values = set(qs.values_list('id', flat=True))
                # qs = qs.filter(id__in=vs_sync)
                # vs = vs.values_list('object_id', flat=True)
                # vs = set(map(int, vs))
                # self.deletados = vs - qs_values

            elif tipo_update == 'get':
                """
                    apesar de a data ser datetime e o campo data_inicio
                    ser DateField, devido a este fato, as partes de um dia
                    é descartada no filtro. 
                """
                q = Q()
                if data_min:
                    q &= Q(data_inicio__gte=data_min)
                if data_max:
                    q &= Q(data_inicio__lte=data_max)

                qs = qs.filter(q)

        return qs
