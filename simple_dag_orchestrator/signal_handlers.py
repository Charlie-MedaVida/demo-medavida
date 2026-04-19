from django.dispatch import receiver

from practices.signals import provider_verify_requested


@receiver(provider_verify_requested)
def on_provider_verify_requested(sender, provider, **kwargs):
    from simple_dag_orchestrator.dags import (
        run_npi_verification,
        run_dea_verification,
    )
    if provider.npi_credential_id:
        run_npi_verification.delay(str(provider.npi_credential_id))
    if provider.dea_credential_id:
        run_dea_verification.delay(str(provider.dea_credential_id))
