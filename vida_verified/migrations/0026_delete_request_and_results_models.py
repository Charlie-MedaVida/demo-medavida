from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0025b_copy_credentials_from_practices'),
    ]

    operations = [
        migrations.DeleteModel(name='MonitorRequest'),
        migrations.DeleteModel(name='ReportRequest'),
        migrations.DeleteModel(name='ReportResults'),
        migrations.DeleteModel(name='MonitorResults'),
    ]
