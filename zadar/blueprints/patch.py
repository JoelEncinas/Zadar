import requests, datetime

from flask import (
    Blueprint, render_template
)

from zadar.blueprints.auth import login_required

bp = Blueprint('patch', __name__, url_prefix='/patch')

base_url = 'https://temtem-api.mael.tech/api'
patch_endpoint = 'patches'
limit = 'limit=1'
type_img_endpoint = 'https://temtem-api.mael.tech/images/icons/types/'

@bp.route('/')
@login_required
def patch():
    url = f"{base_url}/{patch_endpoint}?{limit}"
    response = requests.get(url)
    patch = response.json()[0]

    formatted_date = format_date(patch['date'])

    return render_template('patch/patch.html', patch=patch, date=formatted_date)
    
def format_date(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date.strftime('%d %B %Y').replace(' 0', ' ')

    return formatted_date.replace('{S}', 'th').replace('{st}', 'st').replace('{nd}', 'nd').replace('{rd}', 'rd').replace('{th}', 'th')