SELECT
    c.id,
    c.license_number,
    c.last_checked_at,
    c.enumeration_date,
    c.expiration_date,
    r.checked_at,
    r.verified,
    r.error_content,
    r.json_content
FROM vida_verified_npicredential c
LEFT JOIN vida_verified_npiverificationresult r ON r.id = c.id
