
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from sapl.api.sessao.serializers import SessaoPlenariaOldSerializer,\
    SessaoPlenariaSerializer, ExpedienteMateriaSerializer, OrdemDiaSerializer
from sapl.api.views import TimeRefreshMobileViewSet
from sapl.sessao.models import SessaoPlenaria, ExpedienteMateria, OrdemDia


class SessaoPlenariaOldViewSet(ReadOnlyModelViewSet):

    permission_classes = (AllowAny,)
    serializer_class = SessaoPlenariaOldSerializer
    queryset = SessaoPlenaria.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('data_inicio', 'data_fim', 'interativa')


class SessaoPlenariaViewSet(TimeRefreshMobileViewSet):

    serializer_class = SessaoPlenariaSerializer
    queryset = SessaoPlenaria.objects.all().order_by(
        '-data_inicio', '-hora_inicio')
    field_to_filter_date = 'data_inicio'

    def detail(self, model, serializer_class, **kwargs):
        qs = model.objects.filter(
            sessao_plenaria_id=kwargs['pk']).order_by('numero_ordem')
        self.queryset_refresh(
            qs, field_to_filter_date='sessao_plenaria__data_inicio')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)

    @detail_route()
    def expediente_materia(self, request, *args, **kwargs):
        return self.detail(ExpedienteMateria, **kwargs)

    @detail_route()
    def ordem_dia(self, request, *args, **kwargs):
        return self.detail(OrdemDia, OrdemDiaSerializer, **kwargs)
