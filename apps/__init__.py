import os
import azure.functions as func
import logging
import json
from get_app import get_app_links

def main(req: func.HttpRequest) -> func.HttpResponse:
    response = get_app_links()
    return func.HttpResponse(json.dumps(response),mimetype='application/json')
