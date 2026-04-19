from datetime import datetime

import requests

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
    """
    Validate that response matches the dea_extract_response.json shape,
    then update the DeaCredential record with the extracted values.

    Raises ValueError if the response structure is invalid.
    """
    if 'result' not in response:
        raise ValueError("DEA extraction response missing 'result' key.")

    outer_result = response['result']

    if 'result' not in outer_result or not isinstance(
        outer_result['result'], list
    ):
        raise ValueError(
            "DEA extraction response missing 'result.result' list."
        )

    rows = outer_result['result']
    if not rows:
        raise ValueError("DEA extraction returned no rows.")

    row = rows[0]
    missing = _DEA_EXTRACT_RESULT_KEYS - row.keys()
    if missing:
        raise ValueError(
            f"DEA extraction result missing expected keys: {missing}"
        )

    credential.license_number = row['dea_registration_number']

    expiration = _parse_date(row['this_registration_expires'])
    if expiration:
        credential.expiration_date = expiration

    issue = _parse_date(row['issue_date'])
    if issue:
        credential.enumeration_date = issue

    credential.save()


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
