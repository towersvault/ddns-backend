from flask import Blueprint
from flask import current_app

from ddns import utils
from ddns.db import DataHandler

import click
import os


blueprint = Blueprint('cli', __name__, url_prefix='/cli')


@blueprint.cli.command('create')
@click.argument('subdomain')
def create_cli(subdomain: str):
    """Flask CLI function to create a subdomain record.

    :param subdomain: The subdomain record that should be created.
    """
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
    """Flask CLI function to get information on a subdomain.

    :param subdomain: The subdomain's information that should be retrieved.
    """
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
    """Flask CLI function to reset the API token of a subdomain.

    :param subdomain: The subdomain of which the API token should be reset.
    """
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
    """Flask CLI function to manually set the IP address of a subdomain.

    :param subdomain: The subdomain of which the IP address should be set.
    :param new-ip-address: The IP address that should be used.
    """
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
