from django.conf.urls import include, url

from norma.views import (AssuntoNormaCrud, NormaCrud,
                         NormaPesquisaView, NormaTaView,
                         NormaTemporarioCrud, PesquisaNormaListView,
                         TipoNormaCrud)

from .apps import AppConfig

app_name = AppConfig.name

# @LeandroRoberto comentou em
# https://github.com/interlegis/sapl/pull/255#discussion_r55894269
#
# esse código só está assim de forma temporária, criado no início do
# projeto para apenas dar uma tela básica de listagem de normas para a app
# compilação... a implementação da app norma é independente e não sei em
# que estágio está... para a compilação é relevante apenas que se mantenha
# o código abaixo:
# url(r'^norma/(?P<pk>[0-9]+)/ta$', NormaTaView.as_view(), name='ta')
# bem como a classe NormaTaView que está em norma.views
norma_url_patterns = NormaTemporarioCrud.get_urls() + [
    url(r'^(?P<pk>[0-9]+)/ta$',
        NormaTaView.as_view(), name='ta')
]

urlpatterns = [
    url(r'^norma/', include(NormaCrud.get_urls())),

    url(r'^sistema/norma/tipo/', include(TipoNormaCrud.get_urls())),
    url(r'^sistema/norma/assunto/', include(AssuntoNormaCrud.get_urls())),
    url(r'^norma/pesquisa$',
        NormaPesquisaView.as_view(), name='norma_pesquisa'),
    url(r'^norma/pesquisa-resultado$',
        PesquisaNormaListView.as_view(), name='list_pesquisa_norma'),
]
