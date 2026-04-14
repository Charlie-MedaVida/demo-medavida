import boto3
import json
import logging
from botocore.exceptions import BotoCoreError, ClientError
from django.conf import settings

logger = logging.getLogger(__name__)

_API_CRAWLER_FUNCTION = 'medavida-api-crawler'
_CRAWLER_FUNCTION = 'medavida-crawler'
_ETLS_FUNCTION = 'medavida-etls'
REGION_NAME = 'us-east-2'


def _invoke_lambda(function_name: str, payload: dict) -> dict:
    """Shared low-level helper — invokes a Lambda and returns the parsed response."""
    client = boto3.client(
        'lambda',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME,
    )

    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload).encode('utf-8'),
        )
    except (BotoCoreError, ClientError) as exc:
        logger.exception('Failed to invoke Lambda function %s', function_name)
        raise RuntimeError(f'Lambda invocation failed: {exc}') from exc

    # Function-level errors are surfaced via FunctionError, not HTTP status.
    if response.get('FunctionError'):
        raw = response['Payload'].read().decode('utf-8')
        logger.error(
            'Lambda %s returned a function error: %s', function_name, raw
        )
        raise RuntimeError(
            f'Lambda function error from {function_name}: {raw}'
        )

    return json.loads(response['Payload'].read().decode('utf-8'))


def invoke_api_crawler(crawler: str, params: dict | None = None) -> dict:
    """
    Invoke the medavida-api-crawler Lambda function.

    Args:
        crawler: Dotted module path of the crawler to run
                 (e.g. "npi_registry.search_api_v2_1").
        params:  Optional dict of parameters forwarded to the crawler's
                 run() function.

    Returns:
        The parsed JSON response from the Lambda, in the shape:
            {"crawler": <str>, "result": <dict>}
    """
    payload = {'crawler': crawler, 'params': params or {}}
    result = _invoke_lambda(_API_CRAWLER_FUNCTION, payload)
    logger.info(
        'Lambda %s completed. crawler=%s', _API_CRAWLER_FUNCTION, crawler
    )
    return result


def invoke_etls(etl: str, params: dict | None = None) -> dict:
    """
    Invoke the medavida-etls Lambda function.

    Args:
        etl:    Dotted module path of the ETL to run.
        params: Optional dict of parameters forwarded to the ETL's
                run() function.

    Returns:
        The parsed JSON response from the Lambda.
    """
    payload = {'etl': etl, 'params': params or {}}
    result = _invoke_lambda(_ETLS_FUNCTION, payload)
    logger.info('Lambda %s completed. etl=%s', _ETLS_FUNCTION, etl)
    return result


def invoke_npi_registry_search_crawler(params: list[dict]) -> dict:
    return invoke_api_crawler('npi_registry.search_api_v2_1', params)


def invoke_sam_exclusions_search_crawler(params: list[dict]) -> dict:
    return invoke_api_crawler('sam_exclusions.search', params)


def invoke_npi_registry_search_etl(source_key: str) -> dict:
    return invoke_etls(
        etl='npi_registry_search',
        params={'source_key': source_key},
    )


def invoke_sam_exclusions_search_etl(uuid: str, source_key: str) -> dict:
    return invoke_etls(
        etl='sam_exclusions_search',
        params={'uuid': uuid, 'source_key': source_key},
    )


def invoke_load_credential_report(uuid: str, source_key: str) -> dict:
    return invoke_etls(
        etl='load_credential_report',
        params={'uuid': uuid, 'source_key': source_key},
    )


def invoke_load_credential_monitors() -> dict:
    return invoke_etls(etl='load_credential_monitors')


def invoke_crawler(
    platform: str, bot: str, **kwargs
) -> dict:
    """
    Invoke the medavida-crawler Lambda function.

    Args:
        platform: The target platform/website sub-package to load
                  (e.g. "dea", "npi").
        bot:      The scraper module within that platform to run
                  (e.g. "dea_health_check_scraper").
        **kwargs: Any additional keyword arguments forwarded directly to
                  the scraper's run() classmethod.

    Returns:
        The parsed JSON response returned by the scraper's run() method.
    """
    payload = {'platform': platform, 'bot': bot, **kwargs}
    result = _invoke_lambda(_CRAWLER_FUNCTION, payload)
    logger.info(
        'Lambda %s completed. platform=%s bot=%s',
        _CRAWLER_FUNCTION,
        platform,
        bot,
    )
    return result
