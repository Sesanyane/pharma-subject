from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'pharma_subject'
    verbose_name = 'Pharma Subject'
    admin_site_name = 'pharma_subject_admin'
