import functools

from flask import Blueprint, jsonify, request


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
    
    print(f'API Token: {api_token}')

    return 'None'


@blueprint.route('/get', methods=['GET'])
def get():
    pass
