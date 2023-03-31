import requests

from flask import (
    Blueprint, render_template
)

from zadar.blueprints.auth import login_required

bp = Blueprint('type_chart', __name__, url_prefix='/type-chart')

base_url = 'https://temtem-api.mael.tech'
api_endpoint = '/api'
weaknesses_endpoint = '/weaknesses'
type_img_endpoint = f"{base_url}/images/icons/types/"

@bp.route('/')
@login_required
def type_chart():
    weaknesses = get_weaknesses()
    return render_template(
        'type_chart/type_chart.html',
        weaknesses=weaknesses,
        type_img_endpoint=type_img_endpoint)
    
def get_weaknesses():
    url = f"{base_url}{api_endpoint}{weaknesses_endpoint}"
    response = requests.get(url)
    return response.json()