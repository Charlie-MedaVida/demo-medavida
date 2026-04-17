from django.db import migrations, models


def set_uncredentialed_default(apps, schema_editor):
    ProviderByPractice = apps.get_model('practices', 'ProviderByPractice')
    ProviderByPractice.objects.filter(type='default').update(type='uncredentialed')


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0006_rename_providerpractice_to_providerbypractice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providerbypractice',
            name='type',
            field=models.CharField(
                choices=[
                    ('uncredentialed', 'Uncredentialed'),
                    ('default', 'Default'),
                    ('medical_director', 'Medical Director'),
                ],
                default='uncredentialed',
                max_length=20,
            ),
        ),
        migrations.RunPython(set_uncredentialed_default, migrations.RunPython.noop),
    ]
