from django import apps
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def _get_registration_key(model):
    return '%s:%s' % (model._meta.app_label, model._meta.model_name)


def __time_refresh_generate():
    result = {}
    apps_sapl = [apps.apps.get_app_config(n[5:]) for n in settings.SAPL_APPS]

    for app in apps_sapl:
        for model in app.get_models():
            result[_get_registration_key(model)] = timezone.now(
            )

    return result


_time_refresh_models = {}


def time_refresh_models():
    if not _time_refresh_models:
        _time_refresh_models.update(__time_refresh_generate())
    return _time_refresh_models


_time_refresh_reactive_models = {
    'parlamentares:parlamentar': ['base:autor']
}


class AppConfig(apps.AppConfig):
    name = 'sapl.api'
    label = 'api'
    verbose_name = _('API Rest')


@receiver([post_save, post_delete])
def time_refresh_signal(sender, instance, **kwargs):
    if not _time_refresh_models:
        _time_refresh_models.update(__time_refresh_generate())

    chave = _get_registration_key(sender)
    refresh = _time_refresh_models.get(chave, None)

    if refresh:
        _time_refresh_models[chave] = timezone.now()

    for reactive_model in _time_refresh_reactive_models.get(chave, []):
        _time_refresh_models[reactive_model] = _time_refresh_models[chave]
