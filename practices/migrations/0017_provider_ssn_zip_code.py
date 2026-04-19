from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0016_provider_verification_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='ssn',
            field=models.CharField(blank=True, default='', max_length=9),
        ),
        migrations.AddField(
            model_name='provider',
            name='zip_code',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
