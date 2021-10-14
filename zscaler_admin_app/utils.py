import json
from typing import Any, Optional
from typing import Dict
from typing import List

from zscaler_python_sdk import admin
from zscaler_python_sdk import url_categories
from zscaler_python_sdk import url_filtering_rules


def fetch_adminroles(tenant: str = None) -> List[Dict[Any, Any]]:
    adminroles = admin.fetch_adminroles(tenant=tenant)
    return adminroles


def fetch_adminrole_names(tenant: Optional[str] = None) -> List[str]:
    adminroles = admin.fetch_adminroles(tenant=tenant)
    if tenant is not None:
        role_names = [role["name"] for role in adminroles[tenant]]
        return {tenant: role_names}
    else:
        all_tenant_results: Dict[str, List[str]] = {}
        for tenant_name in adminroles.keys():
            all_tenant_results[tenant_name] = [
                role["name"] for role in adminroles[tenant_name]
            ]
        return all_tenant_results


def fetch_adminusers(tenant: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    adminusers = admin.fetch_adminusers(tenant=tenant)
    return adminusers


def fetch_adminuser_names(tenant: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    adminusers = admin.fetch_adminusers(tenant=tenant)
    for tenant_name in adminusers.keys():
        adminusers[tenant_name] = [
            f"{user['userName']} ({user['loginName']})"
            for user in adminusers[tenant_name]
        ]
    return adminusers


def fetch_url_categories() -> List[List[Dict[Any, Any]]]:
    response: List[Dict[Any, Any]] = url_categories.fetch_url_categories()
    return response


def fetch_url_category_names() -> List[str]:
    categories: List[Dict[Any, Any]] = url_categories.fetch_url_categories()
    response: List[str] = []
    for category in categories:
        if "configuredName" not in category.keys():
            response.append(category["id"])
        else:
            response.append(f"{category['id']} ({category['configuredName']})")
    return response


def create_custom_url_category(
    source_file_path: Optional[str] = None,
    configured_name: Optional[str] = None,
    urls: Optional[List[str]] = None,
    db_categorized_urls: Optional[List[str]] = None,
    description: Optional[str] = None,
) -> str:
    if source_file_path:
        with open(source_file_path) as file:
            parameters = json.load(file)
            configured_name = parameters["configuredName"]
            urls = parameters["urls"]
            db_categorized_urls = parameters["dbCategorizedUrls"]
            description = parameters["description"]

    message = url_categories.create_custom_url_category(
        configured_name,
        urls,
        db_categorized_urls,
        description,
    )
    return message


def fetch_urlfiltering_rule_names() -> List[str]:
    url_filter_rules = url_filtering_rules.fetch_all_url_filering_rules()
    names_of_urlfilter_rules = [
        (
            f"{rule['name']} (Order: {rule['order']}, Action: {rule['action']}, "
            f"Status: {rule['state']})"
        )
        for rule in url_filter_rules
    ]
    return names_of_urlfilter_rules


def fetch_urlfiltering_rule_details() -> List[str]:
    url_filter_rules = url_filtering_rules.fetch_all_url_filering_rules()
    return url_filter_rules
