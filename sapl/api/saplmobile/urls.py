from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from sapl.api.saplmobile.views import SessaoPlenariaViewSet,\
    TimeRefreshDatabaseView, MateriaLegislativaViewSet, AutorViewSet

# Não adicione app_name
# app_name = AppConfig.name

router = SimpleRouter()
router.register(r'sessaoplenaria', SessaoPlenariaViewSet)
router.register(r'materialegislativa', MateriaLegislativaViewSet)
router.register(r'autor', AutorViewSet)

urlpatterns_router = router.urls

urlpatterns_sapl_mobile = [
    url(r'time_refresh$',
        TimeRefreshDatabaseView.as_view(), name="time_refresh"),
]

urlpatterns = [
    url(r'^mobile/', include(urlpatterns_sapl_mobile)),
    url(r'^mobile/', include(urlpatterns_router)),
]
