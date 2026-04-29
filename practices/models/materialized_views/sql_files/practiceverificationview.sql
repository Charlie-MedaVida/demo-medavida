SELECT
    p.id AS id,
    CASE
        WHEN bool_or(
            prov.npi_verification_status = 'running'
            OR prov.dea_verification_status = 'running'
        ) THEN 'running'
        WHEN bool_or(
            prov.npi_verification_status = 'failed'
            OR prov.dea_verification_status = 'failed'
        ) THEN 'failed'
        WHEN count(prov.id) > 0
            AND bool_and(
                prov.npi_verification_status = 'verified'
                AND prov.dea_verification_status = 'verified'
            ) THEN 'verified'
        ELSE 'pending'
    END AS verification_status
FROM practices_practice p
LEFT JOIN practices_providerbypractice pbp ON pbp.practice_id = p.id
LEFT JOIN practices_provider prov ON prov.id = pbp.provider_id
GROUP BY p.id
