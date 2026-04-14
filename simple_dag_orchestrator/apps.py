from django.apps import AppConfig


class SimpleDagOrchestratorConfig(AppConfig):
    name = 'simple_dag_orchestrator'

    def ready(self):
        import simple_dag_orchestrator.signal_handlers  # noqa: F401
