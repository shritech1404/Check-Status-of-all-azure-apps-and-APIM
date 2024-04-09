import os
import azure.functions as func
import logging
import json
from dotenv import load_dotenv
from healthcheck import HealthCheck, EnvironmentDump
from params.required_parameters import env_credentials

health = HealthCheck()
envdump = EnvironmentDump()

load_dotenv(env_credentials)
environment = os.environ["environment_name"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    errors = {}
    if not environment:
        errors['environment'] = 'Error'
        return func.HttpResponse(json.dumps(errors),mimetype='application/json', status_code=500)
    else:
        errors['environment'] = environment
        return func.HttpResponse(json.dumps(errors),mimetype='application/json', status_code=200)

health.add_check(main)