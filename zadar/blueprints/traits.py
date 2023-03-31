import requests

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from zadar.blueprints.auth import login_required

bp = Blueprint('traits', __name__, url_prefix='/trait')

base_url = 'https://temtem-api.mael.tech'
api_endpoint = '/api'
temtems_endpoint = '/temtems'
traits_endpoint = '/traits'
type_img_endpoint = f"{base_url}/images/icons/types/"

@bp.route('/', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        trait_name = request.form.get('trait_name').title()
        return redirect(url_for('traits.trait', name=trait_name))

    traits = get_all_traits()
    return render_template(
        'traits/search.html', 
        traits=traits, 
        type_img_endpoint=type_img_endpoint
    )
    
def get_all_traits():
    url = f"{base_url}{api_endpoint}{traits_endpoint}"
    response = requests.get(url)
    return response.json()

def get_trait(trait):
    response = requests.get(f"{base_url}{api_endpoint}{traits_endpoint}?names={trait}")
    if len(response.json()) == 0:
        return None
    
    return response.json()[0]

def get_temtems_with_trait(trait):
    url = f"{base_url}{api_endpoint}{temtems_endpoint}"
    data = requests.get(url).json()
    temtems = [temtem for temtem in data if trait in temtem['traits']]
    return temtems

def debug_trait(trait_name):
    # traits api bugfix
    if trait_name == 'Attack T':
        trait_name = 'Attack<T>'

    return trait_name

@bp.route('/not_found', methods=('GET', 'POST'))
@login_required
def not_found():
    if request.method == 'POST':
        trait_name = request.form.get('trait_name').title()
        return redirect(url_for('traits.trait', name=trait_name))

    traits = get_all_traits()
    return render_template('traits/not_found.html', traits=traits)

@bp.route('/<name>')
@login_required
def trait(name):
    trait = get_trait(name)

    if trait is None:
            return redirect(url_for('traits.not_found'))

    trait_name = trait['name']
    trait_name = debug_trait(trait_name)

    temtems_data = get_temtems_with_trait(trait_name)

    return render_template(
        'traits/trait.html',
        trait=trait, 
        temtems=temtems_data,
        images_endpoint=base_url,
        type_img_endpoint=type_img_endpoint)
