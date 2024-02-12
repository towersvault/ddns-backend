from flask import Blueprint, jsonify, request, Response, current_app

from ddns.db import DataHandler
from ddns import exceptions

import logging


blueprint = Blueprint('record', __name__, url_prefix='/record')


@blueprint.route('/update', methods=['GET', 'POST'])
def update():
    """
    Updates the provided API token's record to the IP address collected.
    """
    if request.method == 'POST':
        api_token = request.form['api_token']
    else:
        api_token = request.args.get('api_token')

    database = DataHandler(current_app.config['DATABASE'])

    ip_addr = request.remote_addr

    logging.info(f'Update DNS for TOKEN:{api_token} to IP:{ip_addr}')
    
    try:
        database.update_record(api_token, ip_addr)
    except exceptions.APITokenNotFoundError as e:
        logging.error(f'/record/update [{request.method}]: {str(e)}')

        return Response('API token not authorized.', status=401)

    return Response(status=200)


@blueprint.route('/get', methods=['GET'])
def get():
    pass


@blueprint.route('/create', methods=['POST'])
def create():
    pass
