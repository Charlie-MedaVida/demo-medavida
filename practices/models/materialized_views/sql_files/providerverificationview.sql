SELECT
    p.id,
    p.first_name,
    p.last_name,
    p.email,
    p.phone_number,
    p.title,
    p.specialty,
    p.npi_verification_status,
    p.dea_verification_status,
    p.npi_credential_id,
    npi.license_number           AS npi_license_number,
    npi.verified                 AS npi_verified,
    npi.checked_at               AS npi_checked_at,
    npi.enumeration_date         AS npi_enumeration_date,
    npi.expiration_date          AS npi_expiration_date,
    npi.error_content            AS npi_error_content,
    p.dea_credential_id,
    dea.license_number           AS dea_license_number,
    dea.verified                 AS dea_verified,
    dea.checked_at               AS dea_checked_at,
    dea.enumeration_date         AS dea_enumeration_date,
    dea.expiration_date          AS dea_expiration_date,
    dea.error_content            AS dea_error_content
FROM practices_provider p
LEFT JOIN vida_verified_npiverificationview npi ON npi.id = p.npi_credential_id
LEFT JOIN vida_verified_deaverificationview dea ON dea.id = p.dea_credential_id
