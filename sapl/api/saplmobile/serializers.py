from datetime import datetime
import os

from django.utils.timezone import make_aware
from rest_framework import serializers

from sapl.materia.models import MateriaLegislativa
from sapl.sessao.models import SessaoPlenaria, OrdemDia, ExpedienteMateria,\
    RegistroVotacao


class SessaoPlenariaSerializer(serializers.ModelSerializer):
    sessao_legislativa = serializers.StringRelatedField(many=False)
    legislatura = serializers.StringRelatedField(many=False)
    tipo = serializers.StringRelatedField(many=False)

    class Meta:
        model = SessaoPlenaria
        fields = ('id',
                  'sessao_legislativa',
                  'legislatura',
                  'tipo',
                  'data_inicio',
                  'data_fim',
                  'hora_inicio',
                  'hora_fim',
                  'numero',)


class MateriaLegislativaSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('id',
                  'tipo',
                  'tipo_sigla',
                  'numero',
                  'ano',
                  'numero_protocolo',
                  'data_apresentacao',
                  'ementa',
                  'texto_original',
                  'autores',
                  )


class RegistroVotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroVotacao
        fields = '__all__'


class SessaoSerializerMixin(serializers.ModelSerializer):
    materia = MateriaLegislativaSerializer()
    votacao = RegistroVotacaoSerializer(
        many=True, source='registrovotacao_set')

    class Meta:
        fields = ('id',
                  'materia',
                  'observacao',
                  'numero_ordem',
                  'resultado',
                  'tipo_votacao',
                  'sessao_plenaria',
                  'votacao')


class ExpedienteMateriaSerializer(SessaoSerializerMixin):
    class Meta(SessaoSerializerMixin.Meta):
        model = ExpedienteMateria


class OrdemDiaSerializer(SessaoSerializerMixin):
    class Meta(SessaoSerializerMixin.Meta):
        model = OrdemDia
