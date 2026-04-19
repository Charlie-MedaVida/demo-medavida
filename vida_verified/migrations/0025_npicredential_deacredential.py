import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0024_remove_monitorresults_request_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NpiCredential',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4, editable=False, primary_key=True,
                    serialize=False,
                )),
                ('license_number', models.CharField(
                    blank=True, default='', max_length=100,
                )),
                ('last_checked_at', models.DateTimeField(
                    blank=True, null=True,
                )),
                ('enumeration_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('file', models.FileField(
                    blank=True, null=True, upload_to='credentials/',
                )),
            ],
            options={'abstract': False},
        ),
        migrations.CreateModel(
            name='DeaCredential',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4, editable=False, primary_key=True,
                    serialize=False,
                )),
                ('license_number', models.CharField(
                    blank=True, default='', max_length=100,
                )),
                ('last_checked_at', models.DateTimeField(
                    blank=True, null=True,
                )),
                ('enumeration_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('file', models.FileField(
                    blank=True, null=True, upload_to='credentials/',
                )),
            ],
            options={'abstract': False},
        ),
    ]
