import requests

from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from zadar.blueprints.auth import login_required

bp = Blueprint('tempedia', __name__, url_prefix='/tempedia')

base_url = 'https://temtem-api.mael.tech'
api_endpoint = '/api'
temtems_endpoint = '/temtems'
type_img_endpoint = f"{base_url}/images/icons/types/"

@bp.route('/', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        temtem_name = request.form.get('temtem_name').capitalize()
        return redirect(url_for('tempedia.temtem', name=temtem_name))

    temtems = get_all_temtems()
    return render_template(
        'tempedia/search.html', 
        temtems=temtems, 
        images_endpoint=base_url, 
        type_img_endpoint=type_img_endpoint)
     
def get_all_temtems():
    url = f"{base_url}{api_endpoint}{temtems_endpoint}"
    response = requests.get(url)
    return response.json()

def get_temtem_name(temtem):
    response = requests.get(f"{base_url}{api_endpoint}{temtems_endpoint}?names={temtem}")
    if len(response.json()) == 0:
        return None
    
    return response.json()[0]

def get_temtem_number(number):
    response = requests.get(f"{base_url}{api_endpoint}{temtems_endpoint}/{number}")
    
    return response.json()

@bp.route('/not_found', methods=('GET', 'POST'))
@login_required
def not_found():
    if request.method == 'POST':
        temtem_name = request.form.get('temtem_name').capitalize()
        return redirect(url_for('tempedia.temtem', name=temtem_name))

    temtems = get_all_temtems()
    return render_template(
        'tempedia/not_found.html',
        temtems=temtems,
        images_endpoint=base_url, 
        type_img_endpoint=type_img_endpoint)

@bp.route('/<name>')
@login_required
def temtem(name):
    temtem = get_temtem_name(name)

    if temtem is None:
            return redirect(url_for('tempedia.not_found'))

    else:
        next_temtem = 0
        previous_temtem = 0

        if(temtem['number'] == 1):
            previous_temtem = None
            next_temtem = get_temtem_number(2)
        
        elif(temtem['number'] > 1 and temtem['number'] < 164):
            previous_temtem = get_temtem_number(temtem['number'] - 1)
            next_temtem = get_temtem_number(temtem['number'] + 1)

        else:
            previous_temtem = get_temtem_number(163)
            next_temtem = None

        return render_template('tempedia/temtem.html', 
                               temtem=temtem, 
                               type_img_endpoint=type_img_endpoint, 
                               prev=previous_temtem, 
                               next=next_temtem)
    
