import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Moves NpiCredential and DeaCredential from the practices app to
    vida_verified. The DB tables were renamed by vida_verified 0025;
    this migration updates the FK references on Provider and removes
    the old model state from practices.
    """

    dependencies = [
        ('practices', '0017_provider_ssn_zip_code'),
        ('vida_verified', '0025_npicredential_deacredential'),
    ]

    operations = [
        # Re-point the FKs to the vida_verified tables
        migrations.AlterField(
            model_name='provider',
            name='npi_credential',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='primary_providers',
                to='vida_verified.npicredential',
            ),
        ),
        migrations.AlterField(
            model_name='provider',
            name='dea_credential',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='primary_providers',
                to='vida_verified.deacredential',
            ),
        ),
        # Remove the old model state from practices (tables already gone)
        migrations.DeleteModel(name='NpiCredential'),
        migrations.DeleteModel(name='DeaCredential'),
    ]
