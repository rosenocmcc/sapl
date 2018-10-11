
from datetime import datetime

from django.db.models import Q
from django.utils.timezone import utc
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from reversion.models import Version

from sapl.api.apps import _time_refresh_models
from sapl.api.saplmobile.serializers import SessaoPlenariaSerializer,\
    OrdemDiaSerializer, ExpedienteMateriaSerializer,\
    MateriaLegislativaSerializer
from sapl.materia.models import MateriaLegislativa
from sapl.sessao.models import SessaoPlenaria, ExpedienteMateria, OrdemDia


class TimeRefreshDatabaseView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response(_time_refresh_models)


class TimeRefreshMobileMixin(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    deletados = None

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.data['deleted'] = self.deletados if self.deletados else []
        return response

    def get_queryset(self):
        return self.queryset_refresh()

    def queryset_refresh(self, queryset=None, **kwargs):

        qs = queryset if queryset else super().get_queryset()
        opts = qs.model._meta

        data_min = self.request.query_params.get(
            'data_min', kwargs.get('data_min', None))
        data_max = self.request.query_params.get(
            'data_max', kwargs.get('data_max', None))
        tipo_update = self.request.query_params.get(
            'tipo_update', kwargs.get('tipo_update', 'get'))

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

            elif tipo_update in ('get', 'last_items', 'first_items'):
                """
                    se a data for datetime e o campo DateField
                    as partes de um dia são descartadas no filtro. 
                """
                params = {}
                field_to_filter_date = kwargs.get(
                    'field_to_filter_date', self.field_to_filter_date)

                if data_min:
                    params['{}__gte'.format(
                        field_to_filter_date)] = data_min
                if data_max:
                    params['{}__lte'.format(
                        field_to_filter_date)] = data_max

                qs = qs.filter(**params)

        if tipo_update == 'first_items':
            qs = qs[:self.paginator.page_size]
        elif tipo_update == 'last_items':
            qs = qs[self.paginator.page_size * (-1):]
        elif tipo_update == 'get_initial':
            qs = qs[:self.paginator.page_size]

        return qs


class SessaoPlenariaViewSet(TimeRefreshMobileMixin):

    serializer_class = SessaoPlenariaSerializer
    queryset = SessaoPlenaria.objects.all().order_by(
        '-data_inicio', '-hora_inicio')
    field_to_filter_date = 'data_inicio'

    def detail(self, model, serializer_class, **kwargs):
        qs = model.objects.filter(
            sessao_plenaria_id=kwargs['pk']).order_by('numero_ordem')
        qs = self.queryset_refresh(
            qs, field_to_filter_date='sessao_plenaria__data_inicio')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)

    @detail_route()
    def expediente_materia(self, request, *args, **kwargs):
        return self.detail(ExpedienteMateria,
                           ExpedienteMateriaSerializer,
                           **kwargs)

    @detail_route()
    def ordem_dia(self, request, *args, **kwargs):
        return self.detail(OrdemDia,
                           OrdemDiaSerializer,
                           **kwargs)


class MateriaLegislativaViewSet(TimeRefreshMobileMixin):
    serializer_class = MateriaLegislativaSerializer
    queryset = MateriaLegislativa.objects.all().order_by('-data_apresentacao')
