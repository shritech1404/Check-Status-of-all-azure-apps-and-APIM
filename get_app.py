import requests
import os
from dotenv import load_dotenv
from params.required_parameters import env_credentials
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient

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

    # Authenticate to Azure
    client = ResourceManagementClient(credentials, subscription_id)
    resource_groups = client.resource_groups.list()

    apps, app_names, results = [], [], []
    for resource_group in resource_groups:
        # List resources in the specified resource group
        for resource in client.resources.list_by_resource_group(resource_group.name):
            if resource.type in ['Microsoft.Web/sites', 'Microsoft.Web/sites/functions']:
                apps.append(f'https://{resource.name}.azurewebsites.net')
                app_names.append(resource.name)
    print(apps)
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
