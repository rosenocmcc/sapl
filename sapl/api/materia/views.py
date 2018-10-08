from django_filters.rest_framework.backends import DjangoFilterBackend

from sapl.api.materia.serializers import MateriaLegislativaSerializer
from sapl.api.views import TimeRefreshMobileViewSet
from sapl.materia.models import MateriaLegislativa


class MateriaLegislativaViewSet(TimeRefreshMobileViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('numero', 'ano', 'tipo', )

    serializer_class = MateriaLegislativaSerializer

    queryset = MateriaLegislativa.objects.all().order_by(
        '-data_apresentacao')
    field_to_filter_date = 'data_apresentacao'
