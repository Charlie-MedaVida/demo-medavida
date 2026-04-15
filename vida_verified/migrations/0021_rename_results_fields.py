from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0020_baseresults_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportresults',
            old_name='sam_exclusions',
            new_name='sam_exclusions_results',
        ),
        migrations.RenameField(
            model_name='reportresults',
            old_name='npi_registration',
            new_name='npi_registration_results',
        ),
        migrations.RenameField(
            model_name='monitorresults',
            old_name='sam_exclusions',
            new_name='sam_exclusions_results',
        ),
        migrations.RenameField(
            model_name='monitorresults',
            old_name='npi_registration',
            new_name='npi_registration_results',
        ),
    ]