from flask import Blueprint, jsonify, request, Response, current_app

from ddns.db import DataHandler
from ddns import exceptions
from ddns import utils

import click
import logging
import os


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


@blueprint.cli.command('create-dns')
@click.argument('subdomain')
def create_cli(subdomain: str):
    database = DataHandler(current_app.config['DATABASE'])
    full_dns_record = f'{subdomain}.{os.getenv("DOMAIN_NAME")}'

    if database.dns_record_exists(full_dns_record):
        click.echo(f'DNS record "{full_dns_record}" already exists.')
        return
    
    api_token = utils.generate_full_token_pair()
    database.create_new_record(
        dns_record=full_dns_record,
        api_token=api_token
    )

    click.echo(f'DNS record "{full_dns_record}" created!')
    click.echo(f'API token: {api_token}')
