import requests

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from zadar.blueprints.auth import login_required

bp = Blueprint('techniques', __name__, url_prefix='/techniques')

base_url = 'https://temtem-api.mael.tech'
api_endpoint = '/api'
temtems_endpoint = '/temtems'
techniques_endpoint = '/techniques'
type_img_endpoint = f"{base_url}/images/icons/types/"
     
@bp.route('/', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        technique_name = request.form.get('technique_name').title()

        return redirect(url_for('techniques.technique', name=technique_name))

    techniques = get_all_techniques()
    return render_template(
        'techniques/search.html', 
        techniques=techniques, 
        type_img_endpoint=type_img_endpoint,
        base_url=base_url)

def get_all_techniques():
    url = f"{base_url}{api_endpoint}{techniques_endpoint}"
    response = requests.get(url)
    return response.json()

def get_technique(technique_name):
    technique = uppercase_technique(technique_name)
    response = requests.get(f"{base_url}{api_endpoint}{techniques_endpoint}?names={technique}")
    if len(response.json()) == 0:
        return None
    
    return response.json()[0]

def get_temtems_with_technique(technique):
    url = f"{base_url}{api_endpoint}{temtems_endpoint}"
    data = requests.get(url).json()
    temtems = [temtem for temtem in data if technique['name'] in [technique["name"] for technique in temtem["techniques"]]]
    return temtems

def uppercase_technique(technique_name):
    # techniques api bugfix
    if technique_name == 'Dc Beam':
        technique_name = 'DC Beam'
    if technique_name == '5Ppeh':
        technique_name = '5PPEH'
    if technique_name == 'Dna Extraction':
        technique_name = 'DNA Extraction'

    return technique_name

@bp.route('/not_found', methods=('GET', 'POST'))
@login_required
def not_found():
    if request.method == 'POST':
        technique_name = request.form.get('technique_name').title()
        return redirect(url_for('techniques.technique', name=technique_name))

    techniques = get_all_techniques()
    return render_template(
        'techniques/not_found.html', 
        techniques=techniques, 
        type_img_endpoint=type_img_endpoint,
        base_url=base_url)

@bp.route('/<name>')
@login_required
def technique(name):
    technique = get_technique(name)

    if technique is None:
        return redirect(url_for('techniques.not_found'))

    temtems_data = get_temtems_with_technique(technique)
    
    return render_template(
        'techniques/technique.html',
        technique=technique,
        temtems=temtems_data, 
        images_endpoint=base_url,
        type_img_endpoint=type_img_endpoint)