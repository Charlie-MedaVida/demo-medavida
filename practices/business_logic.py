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
