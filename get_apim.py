import requests
import os
from dotenv import load_dotenv
from params.required_parameters import env_credentials
from azure.identity import ClientSecretCredential
from azure.mgmt.apimanagement import ApiManagementClient

load_dotenv(env_credentials)
tenant_id = os.environ["tenant_id"]
client_id = os.environ["client_id"]
client_secret = os.environ["client_secret"]

# Azure API Management details
apim_service_name = os.environ["apim_service_name"]
resource_group_name = os.environ["resource_group_name"]
subscription_id = os.environ["subscription_id"]
apim_instance_url = f'https://{apim_service_name}.azure-api.net'

def get_app_links():
    credentials = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    client = ApiManagementClient(credentials, subscription_id=subscription_id)
    apis = client.api.list_by_service(resource_group_name, apim_service_name)

    apps, app_names, results = [], [], []
    for api in apis:
        apps.append(f'{apim_instance_url}/{api.name}')
        app_names.append(api.name)
    count = 0
    for app in apps:
        if app_names[count]=='dmdcs':
            app = f'{app}/testing'
        else:
            app = f'{app}/healthcheck'
        response = requests.get(app)
        if response.status_code==200:
            results.append({'app_name':app_names[count], 'status':'up', 'message':'app is running','status_code':response.status_code})
        else:
            results.append({'app_name':app_names[count], 'status':'down', 'message':'app is not running','status_code':response.status_code, 'reason':response.reason})
        count += 1
    return results


