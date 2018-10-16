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
            ).isoformat(timespec='milliseconds')[:-6]

    return result


time_refresh_models = {}


class AppConfig(apps.AppConfig):
    name = 'sapl.api'
    label = 'api'
    verbose_name = _('API Rest')


@receiver([post_save, post_delete])
def time_refresh_signal(sender, instance, **kwargs):
    if not time_refresh_models:
        time_refresh_models.update(__time_refresh_generate())

    refresh = time_refresh_models.get(_get_registration_key(sender), None)

    if refresh:
        time_refresh_models[_get_registration_key(
            sender)] = timezone.now().isoformat(timespec='milliseconds')[:-6]
