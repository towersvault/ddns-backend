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

    database = DataHandler(database_name=current_app.config['DATABASE'])

    ip_addr = request.remote_addr

    logging.info(f'Update DNS for TOKEN:{api_token} to IP:{ip_addr}')
    
    try:
        subdomain_record = database.get_bound_subdomain_record(api_token=api_token)
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


@blueprint.cli.command('create')
@click.argument('subdomain')
def create_cli(subdomain: str):
    database = DataHandler(database_name=current_app.config['DATABASE'])

    echo_title = 'DNS Record - Creation'
    full_dns_record = f'{subdomain}.{os.getenv("DOMAIN_NAME")}'

    if database.subdomain_record_exists(subdomain_record=subdomain):
        click.echo((f'{echo_title}\n'
                    f'{"-" * len(echo_title)}\n'
                    f'DNS record "{full_dns_record}" already exists.\n'))
        return
    
    api_token = utils.generate_full_token_pair()
    database.create_new_record(subdomain_record=subdomain, 
                               api_token=api_token)

    click.echo((f'{echo_title}\n'
                f'{"-" * len(echo_title)}\n'
                f'DNS Record: {full_dns_record}\n'
                f'API token: {api_token}\n'))


@blueprint.cli.command('get')
@click.argument('subdomain')
def get_cli(subdomain: str):
    database = DataHandler(database_name=current_app.config['DATABASE'])

    echo_title = 'DNS Record - Information'
    full_dns_record = f'{subdomain}.{os.getenv("DOMAIN_NAME")}'

    if not database.subdomain_record_exists(subdomain_record=subdomain):
        click.echo((f'{echo_title}\n'
                    f'{"-" * len(echo_title)}\n'
                    f'DNS record "{full_dns_record}" doesn\'t exist.\n'))
        return
    
    ddns_record = database.get_record_data(subdomain_record=subdomain)

    click.echo((f'{echo_title}\n'
                f'{"-" * len(echo_title)}\n'
                f'DNS Record: {full_dns_record}\n'
                f'Identifier API Token: {ddns_record.identifier_token}\n'
                f'IP Address: {ddns_record.ip_address}\n'
                f'Last Updated: {ddns_record.last_updated}\n'
                f'Created: {ddns_record.created}\n'))
    

@blueprint.cli.command('reset-api-token')
@click.argument('subdomain')
def reset_api_token_cli(subdomain: str):
    database = DataHandler(database_name=current_app.config['DATABASE'])

    echo_title = 'DNS Record - API Token Reset'
    full_dns_record = f'{subdomain}.{os.getenv("DOMAIN_NAME")}'

    if not database.subdomain_record_exists(subdomain_record=subdomain):
        click.echo((f'{echo_title}\n'
                    f'{"-" * len(echo_title)}'
                    f'DNS record "{full_dns_record}" doesn\'t exist.\n'))
        return
    
    api_token = utils.generate_full_token_pair()
    database.update_record_api_token(subdomain_record=subdomain, 
                                     new_api_token=api_token)

    click.echo((f'{echo_title}\n'
                f'{"-" * len(echo_title)}\n'
                f'API token reset!\n'
                f'DNS Record: {full_dns_record}\n'
                f'New API token: {api_token}\n'))


@blueprint.cli.command('set-ip')
@click.argument('subdomain')
@click.argument('new-ip-address')
def set_ip_cli(subdomain, new_ip_address):
    database = DataHandler(database_name=current_app.config['DATABASE'])

    echo_title = 'DNS Record - Set IP Address'
    full_dns_record = f'{subdomain}.{os.getenv("DOMAIN_NAME")}'

    if not database.subdomain_record_exists(subdomain_record=subdomain):
        click.echo((f'{echo_title}\n'
                    f'{"-" * len(echo_title)}'
                    f'DNS record "{full_dns_record}" doesn\'t exist.\n'))
        return
    
    database.update_record_ip_address(subdomain_record=subdomain, 
                                      ip_address=new_ip_address)

    click.echo((f'{echo_title}\n'
                f'{"-" * len(echo_title)}\n'
                f'IP address set!\n'
                f'DNS Record: {full_dns_record}\n'
                f'New IP Address: {new_ip_address}\n'))
