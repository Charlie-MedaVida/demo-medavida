import uuid

from django.db import migrations, models


def backfill_uuids(apps, schema_editor):
    ReportRequest = apps.get_model('vida_verified', 'ReportRequest')
    MonitorRequest = apps.get_model('vida_verified', 'MonitorRequest')
    for model in (ReportRequest, MonitorRequest):
        for obj in model.objects.all():
            ssn = obj.ssn or 'null'
            ein = obj.ein or 'null'
            id_type = obj.id_type or 'null'
            obj.uuid = uuid.uuid5(uuid.NAMESPACE_OID, f"{id_type}{ssn}{ein}")
            obj.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0018_baserequest_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportrequest',
            name='uuid',
            field=models.UUIDField(editable=False),
        ),
        migrations.AlterField(
            model_name='monitorrequest',
            name='uuid',
            field=models.UUIDField(editable=False),
        ),
        migrations.RunPython(backfill_uuids, migrations.RunPython.noop),
    ]