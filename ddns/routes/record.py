from flask import Blueprint
from flask import request
from flask import Response
from flask import current_app

from ddns import exceptions
from ddns.db import DataHandler

import logging


blueprint = Blueprint('record', __name__, url_prefix='/record')


@blueprint.route('/update', methods=['GET', 'POST'])
def update():
    """HTTP-GET/POST Flask route to update the IP address of a given API token.

    :param api_token: The API token that the IP address should be updated of.
    """
    if request.method == 'POST':
        api_token = request.form['api_token']
    else:
        api_token = request.args.get('api_token')

    database = DataHandler(database_name=current_app.config['DATABASE'])

    ip_addr = request.remote_addr

    logging.info(f'Update DNS for TOKEN:{api_token} to IP:{ip_addr}')

    try:
        subdomain_record = database.get_bound_subdomain_record(
            api_token=api_token)
        database.update_record_ip_address(subdomain_record=subdomain_record,
                                          ip_address=ip_addr)
    except exceptions.IdentifierTokenNotFoundError as e:
        logging.error(f'/record/update [{request.method}]: {str(e)}')

        return Response('API token not authorized.', status=401)
    except exceptions.SecretTokenIncorrectError as e:
        logging.error(f'/record/update [{request.method}]: {str(e)}')

        return Response('API token not authorized.', status=401)

    return Response(status=200)


@blueprint.route('/get', methods=['GET'])
def get():
    pass
