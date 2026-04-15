import uuid

from django.db import migrations, models


def populate_uuids(apps, schema_editor):
    ReportResults = apps.get_model('vida_verified', 'ReportResults')
    MonitorResults = apps.get_model('vida_verified', 'MonitorResults')
    for model in (ReportResults, MonitorResults):
        for obj in model.objects.filter(uuid__isnull=True):
            obj.uuid = uuid.uuid4()
            obj.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0019_baserequest_uuid_hash'),
    ]

    operations = [
        # Step 1: add as nullable without unique constraint
        migrations.AddField(
            model_name='reportresults',
            name='uuid',
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name='monitorresults',
            name='uuid',
            field=models.UUIDField(null=True),
        ),

        # Step 2: populate unique UUIDs for existing rows
        migrations.RunPython(populate_uuids, migrations.RunPython.noop),

        # Step 3: enforce unique and not-null
        migrations.AlterField(
            model_name='reportresults',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='monitorresults',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]