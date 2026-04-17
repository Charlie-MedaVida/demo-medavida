from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0005_providerpractice_alter_provider_practices'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProviderPractice',
            new_name='ProviderByPractice',
        ),
    ]
