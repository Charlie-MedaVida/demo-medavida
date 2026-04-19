import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0026_delete_request_and_results_models'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MonitorResultsView',
        ),
        migrations.DeleteModel(
            name='ReportResultsView',
        ),
        migrations.CreateModel(
            name='NpiVerificationResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('checked_at', models.DateTimeField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('error_content', models.TextField(blank=True, default='')),
                ('json_content', models.TextField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeaVerificationResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('checked_at', models.DateTimeField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('error_content', models.TextField(blank=True, default='')),
                ('json_content', models.TextField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
