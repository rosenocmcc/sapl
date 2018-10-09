from rest_framework import serializers
from sapl.materia.models import MateriaLegislativa
from sapl.sessao.models import SessaoPlenaria, OrdemDia, ExpedienteMateria


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


class ExpedienteMateriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpedienteMateria
        fields = '__all__'


class OrdemDiaSerializer(serializers.ModelSerializer):

    class MateriaLegislativaSerializer(serializers.ModelSerializer):
        tipo = serializers.StringRelatedField(many=False)
        tipo_sigla = serializers.SerializerMethodField()

        class Meta:
            model = MateriaLegislativa
            fields = '__all__'

        def get_tipo_sigla(self, obj):
            return obj.tipo.sigla

    materia = MateriaLegislativaSerializer()

    class Meta:
        model = OrdemDia
        fields = '__all__'
