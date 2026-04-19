from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0015_provider_npi_dea_fks'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='npi_verification_status',
            field=models.CharField(
                blank=True,
                choices=[
                    ('running', 'Running'),
                    ('verified', 'Verified'),
                    ('failed', 'Failed'),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='provider',
            name='dea_verification_status',
            field=models.CharField(
                blank=True,
                choices=[
                    ('running', 'Running'),
                    ('verified', 'Verified'),
                    ('failed', 'Failed'),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
