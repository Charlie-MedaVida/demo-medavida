import logging
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

_NPPES_API_URL = 'https://npiregistry.cms.hhs.gov/api/'
_NPPES_PARAMS = {
    'number', 'first_name', 'last_name', 'use_first_name_alias',
    'organization_name', 'city', 'state', 'postal_code', 'country_code',
    'address_purpose', 'enumeration_type', 'taxonomy_description',
    'credentials', 'sole_proprietor', 'limit', 'offset',
}


def nppes_search(params: dict) -> dict:
    payload = {k: v for k, v in params.items() if k in _NPPES_PARAMS}
    payload['version'] = '2.1'
    response = requests.get(_NPPES_API_URL, params=payload, timeout=10)
    response.raise_for_status()
    return response.json()


_DEA_EXTRACT_RESULT_KEYS = {
    'dea_registration_number', 'this_registration_expires', 'issue_date',
    'business_activity', 'schedules', 'full_name', 'company_name',
    'street_address', 'city', 'state', 'postal_code',
}


def _parse_date(value: str):
    for fmt in ('%m-%d-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(value, fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def apply_dea_extraction(response: dict, credential) -> None:
    print("-")
    print("-")
    print("-")
    print("-")
    print(".")
    logger.info(
        'apply_dea_extraction called. credential_id=%s raw_response=%s',
        credential.id, response,
    )

    if 'result' not in response:
        logger.error(
            'apply_dea_extraction: missing top-level result key. '
            'credential_id=%s response_keys=%s',
            credential.id, list(response.keys()),
        )
        raise ValueError("DEA extraction response missing 'result' key.")

    outer_result = response['result']
    logger.debug(
        'apply_dea_extraction: outer_result keys=%s credential_id=%s',
        list(outer_result.keys()), credential.id,
    )

    if 'result' not in outer_result or not isinstance(
        outer_result['result'], list
    ):
        logger.error(
            'apply_dea_extraction: missing or invalid result.result list. '
            'credential_id=%s outer_result_keys=%s',
            credential.id, list(outer_result.keys()),
        )
        raise ValueError(
            "DEA extraction response missing 'result.result' list."
        )

    rows = outer_result['result']
    if not rows:
        logger.error(
            'apply_dea_extraction: result.result list is empty. '
            'credential_id=%s',
            credential.id,
        )
        raise ValueError("DEA extraction returned no rows.")

    row = rows[0]
    logger.info(
        'apply_dea_extraction: extracted row. credential_id=%s row=%s',
        credential.id, row,
    )

    missing = _DEA_EXTRACT_RESULT_KEYS - row.keys()
    if missing:
        logger.error(
            'apply_dea_extraction: row missing expected keys=%s '
            'credential_id=%s',
            missing, credential.id,
        )
        raise ValueError(
            f"DEA extraction result missing expected keys: {missing}"
        )

    credential.license_number = row['dea_registration_number']
    logger.info(
        'apply_dea_extraction: set license_number=%s credential_id=%s',
        credential.license_number, credential.id,
    )

    expiration = _parse_date(row['this_registration_expires'])
    if expiration:
        credential.expiration_date = expiration
        logger.info(
            'apply_dea_extraction: set expiration_date=%s credential_id=%s',
            expiration, credential.id,
        )
    else:
        logger.warning(
            'apply_dea_extraction: could not parse expiration_date from '
            'value=%r credential_id=%s',
            row['this_registration_expires'], credential.id,
        )

    issue = _parse_date(row['issue_date'])
    if issue:
        credential.enumeration_date = issue
        logger.info(
            'apply_dea_extraction: set enumeration_date=%s credential_id=%s',
            issue, credential.id,
        )
    else:
        logger.warning(
            'apply_dea_extraction: could not parse enumeration_date from '
            'value=%r credential_id=%s',
            row['issue_date'], credential.id,
        )

    credential.save()
    logger.info(
        'apply_dea_extraction: credential saved. credential_id=%s',
        credential.id,
    )


def autofill(npi_number: str, credential, provider) -> None:
    data = nppes_search({'number': npi_number})
    results = data.get('results', [])
    if not results:
        return

    result = results[0]
    basic = result.get('basic', {})

    credential.license_number = result.get('number', credential.license_number)
    enumeration_date = result.get('enumeration_date')
    if enumeration_date:
        credential.enumeration_date = enumeration_date
    credential.save()

    provider.first_name = basic.get('first_name', provider.first_name)
    provider.last_name = basic.get('last_name', provider.last_name)
    provider.title = basic.get('credential', provider.title)

    primary_taxonomy = next(
        (t for t in result.get('taxonomies', []) if t.get('primary')), None
    )
    if primary_taxonomy:
        provider.specialty = primary_taxonomy.get('desc', provider.specialty)

    provider.save()
