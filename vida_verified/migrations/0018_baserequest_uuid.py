import uuid

from django.db import migrations, models


def populate_uuids(apps, schema_editor):
    ReportRequest = apps.get_model('vida_verified', 'ReportRequest')
    MonitorRequest = apps.get_model('vida_verified', 'MonitorRequest')
    for model in (ReportRequest, MonitorRequest):
        for obj in model.objects.filter(uuid__isnull=True):
            obj.uuid = uuid.uuid4()
            obj.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0017_monitorresultsview_reportresultsview'),
    ]

    operations = [
        # Step 1: add as nullable (no unique) so existing rows are accepted
        migrations.AddField(
            model_name='reportrequest',
            name='uuid',
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='uuid',
            field=models.UUIDField(null=True),
        ),

        # Step 2: populate a unique UUID for every existing row
        migrations.RunPython(populate_uuids, migrations.RunPython.noop),

        # Step 3: enforce uniqueness and remove null
        migrations.AlterField(
            model_name='reportrequest',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='monitorrequest',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]