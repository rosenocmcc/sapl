from datetime import datetime
import os

from django.utils.timezone import make_aware
from image_cropping.utils import get_backend
from rest_framework import serializers

from sapl.base.models import Autor
from sapl.materia.models import MateriaLegislativa, Autoria
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


class AutorSerializer(serializers.ModelSerializer):
    fotografia = serializers.SerializerMethodField()
    file_date_updated = serializers.SerializerMethodField()

    class Meta:
        model = Autor
        fields = ('id', 'nome', 'fotografia', 'file_date_updated')

    def get_fotografia(self, obj):
        if obj.autor_related:
            if hasattr(obj.autor_related, 'fotografia'):
                thumbnail_url = get_backend().get_thumbnail_url(
                    obj.autor_related.fotografia,
                    {
                        'size': (128, 128),
                        'box':  obj.autor_related.cropping,
                        'crop': True,
                        'detail': True,
                    }
                )

                return thumbnail_url
        return ''

    def get_file_date_updated(self, obj):
        if obj.autor_related:
            if hasattr(obj.autor_related, 'fotografia'):
                file = obj.autor_related.fotografia
                try:
                    lastmodified = os.stat(file.path).st_mtime
                    return make_aware(
                        datetime.utcfromtimestamp(lastmodified)
                    ).isoformat(timespec='milliseconds')[:-6]
                except:
                    return None
        return None


class MateriaLegislativaSerializerMixin(serializers.ModelSerializer):
    tipo = serializers.StringRelatedField(many=False)
    tipo_sigla = serializers.SerializerMethodField()
    file_date_updated = serializers.SerializerMethodField()
    autores = AutorSerializer(many=True)

    class Meta:
        model = MateriaLegislativa
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
                  'file_date_updated'
                  )

    def get_tipo_sigla(self, obj):
        return obj.tipo.sigla

    def get_file_date_updated(self, obj):
        file = obj.texto_original
        try:
            lastmodified = os.stat(file.path).st_mtime
            return make_aware(
                datetime.utcfromtimestamp(lastmodified)
            ).isoformat(timespec='milliseconds')[:-6]
        except Exception as e:
            return None


class MateriaLegislativaSerializer(MateriaLegislativaSerializerMixin):
    anexadas = MateriaLegislativaSerializerMixin(many=True)
    anexo_de = MateriaLegislativaSerializerMixin(many=True)

    class Meta(MateriaLegislativaSerializerMixin.Meta):

        fields = ('id',
                  'tipo',
                  'tipo_sigla',
                  'numero',
                  'ano',
                  'numero_protocolo',
                  'data_apresentacao',
                  'ementa',
                  'texto_original',
                  'anexadas',
                  'anexo_de',
                  'autores',
                  'file_date_updated'
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
