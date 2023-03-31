import requests

from flask import (
    Blueprint, render_template, request
)

from zadar.blueprints.auth import login_required

bp = Blueprint('weaknesses_calculator', __name__, url_prefix='/calculator')

base_url = 'https://temtem-api.mael.tech'
api_endpoint = '/api'
types_endpoint = '/types'
calculate_endpoint = '/weaknesses/calculate/'
type_img_endpoint = f"{base_url}/images/icons/types/"

@bp.route('/', methods=('GET', 'POST'))
@login_required
def calculate():
    types_data = requests.get(f"{base_url}{api_endpoint}{types_endpoint}").json()
    types = {type_data['name'] for type_data in types_data}

    if request.method == 'POST':
        attacking = request.form.get('attacking')
        defending1 = request.form.get('defending1')
        defending2 = request.form.get('defending2')

        if(defending2 == "no-type"):
            response = requests.post(f"{base_url}{api_endpoint}{calculate_endpoint}?attacking={attacking}&defending={defending1}")
            data = response.json()
            return render_template('weaknesses_calculator/result.html', result=data, type_img_endpoint=type_img_endpoint)
        else:
            response = requests.post(f"{base_url}{api_endpoint}{calculate_endpoint}?attacking={attacking}&defending={defending1},{defending2}")
            data = response.json()
            return render_template('weaknesses_calculator/result.html', result=data, type_img_endpoint=type_img_endpoint)

    return render_template('weaknesses_calculator/calculate.html', types=types)