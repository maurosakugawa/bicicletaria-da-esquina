from django.apps import AppConfig

class OrdemServicoConfig(AppConfig):
    name = 'ordens_servico'

    def ready(self):
        import ordens_servico.signals
