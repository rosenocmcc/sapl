from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from sapl.api.saplmobile.views import SessaoPlenariaViewSet,\
    TimeRefreshDatabaseView

# Não adicione app_name
# app_name = AppConfig.name

router = SimpleRouter()
router.register(r'sessao-plenaria', SessaoPlenariaViewSet)

urlpatterns_router = router.urls

urlpatterns_sapl_mobile = [
    url(r'time_refresh$',
        TimeRefreshDatabaseView.as_view(), name="time_refresh"),
]

urlpatterns = [
    url(r'^mobile/', include(urlpatterns_sapl_mobile)),
    url(r'^mobile/', include(urlpatterns_router)),
]
