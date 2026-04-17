from django.db import migrations


def backfill_uncredentialed(apps, schema_editor):
    Provider = apps.get_model('practices', 'Provider')
    Provider.objects.filter(title='').update(title='Uncredentialed')


class Migration(migrations.Migration):

    dependencies = [
        ('practices', '0010_alter_provider_title_default'),
    ]

    operations = [
        migrations.RunPython(backfill_uncredentialed, migrations.RunPython.noop),
    ]
