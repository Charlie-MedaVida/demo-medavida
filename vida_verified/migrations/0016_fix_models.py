import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0015_reportresults_delete_onetimereport'),
    ]

    operations = [

        # ── ReportRequest ────────────────────────────────────────────────────

        migrations.RemoveField(
            model_name='reportrequest',
            name='user',
        ),
        migrations.AlterField(
            model_name='reportrequest',
            name='status',
            field=models.CharField(
                choices=[
                    ('PENDING', 'Pending'),
                    ('RUNNING', 'Running'),
                    ('PROCESSING', 'Processing'),
                    ('COMPLETE', 'Complete'),
                    ('FAILED', 'Failed'),
                ],
                default='PENDING',
                max_length=24,
            ),
        ),

        # ── MonitorRequest ───────────────────────────────────────────────────

        migrations.AddField(
            model_name='monitorrequest',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='state',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='ssn',
            field=models.CharField(blank=True, default='', max_length=11),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='ein',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='id_type',
            field=models.CharField(
                blank=True,
                choices=[('SSN', 'SSN'), ('EIN', 'EIN')],
                default='',
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='status',
            field=models.CharField(
                choices=[
                    ('PENDING', 'Pending'),
                    ('RUNNING', 'Running'),
                    ('PROCESSING', 'Processing'),
                    ('COMPLETE', 'Complete'),
                    ('FAILED', 'Failed'),
                ],
                default='PENDING',
                max_length=24,
            ),
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitorrequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),

        # ── ReportResults ────────────────────────────────────────────────────

        migrations.RemoveField(
            model_name='reportresults',
            name='request',
        ),
        migrations.AddField(
            model_name='reportresults',
            name='request_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportresults',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportresults',
            name='sam_exclusions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reportresults',
            name='npi_registration',
            field=models.TextField(blank=True, null=True),
        ),

        # ── MonitorResults ───────────────────────────────────────────────────

        migrations.RemoveField(
            model_name='monitorresults',
            name='request',
        ),
        migrations.AddField(
            model_name='monitorresults',
            name='request_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monitorresults',
            name='sam_exclusions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='monitorresults',
            name='npi_registration',
            field=models.TextField(blank=True, null=True),
        ),
    ]
