from django.db import migrations


def copy_credentials_forward(apps, schema_editor):
    db = schema_editor.connection.alias

    OldNpi = apps.get_model('practices', 'NpiCredential')
    NewNpi = apps.get_model('vida_verified', 'NpiCredential')
    for row in OldNpi.objects.using(db).all():
        NewNpi.objects.using(db).get_or_create(
            id=row.id,
            defaults=dict(
                license_number=row.license_number,
                last_checked_at=row.last_checked_at,
                enumeration_date=row.enumeration_date,
                expiration_date=row.expiration_date,
                file=row.file,
            ),
        )

    OldDea = apps.get_model('practices', 'DeaCredential')
    NewDea = apps.get_model('vida_verified', 'DeaCredential')
    for row in OldDea.objects.using(db).all():
        NewDea.objects.using(db).get_or_create(
            id=row.id,
            defaults=dict(
                license_number=row.license_number,
                last_checked_at=row.last_checked_at,
                enumeration_date=row.enumeration_date,
                expiration_date=row.expiration_date,
                file=row.file,
            ),
        )


class Migration(migrations.Migration):

    dependencies = [
        ('vida_verified', '0025_npicredential_deacredential'),
        ('practices', '0017_provider_ssn_zip_code'),
    ]

    operations = [
        migrations.RunPython(
            copy_credentials_forward,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
