import requests, json
from flask import g, jsonify, request
from . import main
from .. import db, cache
from ..email import send_email
from ..models import User
from ..api.authentication import auth


@main.route('/', methods=['GET'])
@cache.cached(timeout=3600)
def index():
    return '<h1>EatPotTeam Movie Ticketing Server</h1>'


@main.route('/auth/register', methods=['POST'])
def register():
    detail = request.json
    if not detail:
        return jsonify({
            'error': 'register fail!'
        }), 400
    user_email = detail['email']
    user_password = detail['password']
    if User.query.filter_by(email=user_email).first() is not None:
        return jsonify({
            'error': 'email is used!'
        }), 409
    user = User(email=user_email, password=user_password)
    db.session.add(user)
    db.session.commit()
    token = user.generate_confirmation_token()
    send_email(user.email, 'Confirm Your Account', 'auth/email/confirm',
               user=user, token=token)
    return jsonify({
        'result': 'success'
    })


@main.route('/confirm/<token>')
def confirm(token):
    if User.confirm(token):
        return jsonify({
            'result': 'success'
        })
    else:
        return jsonify({
            'error': 'The confirmation link is invalid or has expired.'
        }), 401


@main.route('/confirm')
@auth.login_required
def resend_confirmation():
    current_user = g.current_user
    token = current_user.generate_confirmation_token()
    send_email(g.current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    return jsonify({
        'result': 'success'
    })


@main.route('/movie', methods=['GET'])
@cache.cached(timeout=3600)
def get_today_movies():
    url = 'http://localhost:5000/api/movie'
    res = requests.get(url=url)
    return jsonify(res.json())


@main.route('/movie/<int:id>', methods=['GET'])
@cache.cached(timeout=3600)
def get_movie_by_id(id):
    url = 'http://localhost:5000/api/movie/' + str(id)
    res = requests.get(url=url)
    return jsonify(res.json())


@main.route('/cinema', methods=['GET'])
@cache.cached(timeout=3600)
def get_all_cinema():
    url = 'http://localhost:5000/api/cinema'
    res = requests.get(url=url)
    return jsonify(res.json())


@main.route('/cinema/<int:id>', methods=['GET'])
@cache.cached(timeout=3600)
def get_cinema_broadcast(id):
    url = 'http://localhost:5000/api/cinema/' + str(id)
    res = requests.get(url=url)
    return jsonify(res.json())


@main.route('/movie/<int:id>/cinema', methods=['GET'])
@cache.cached(timeout=3600)
def get_movie_on_cinema(id):
    url = 'http://localhost:5000/api/movie/' + str(id) + '/cinema'
    res = requests.get(url=url)
    return jsonify(res.json())


@main.route('/broadcast/<int:id>', methods=['GET'])
def get_seats(id):
    url = 'http://localhost:5000/api/broadcast/' + str(id)
    res = requests.get(url=url)
    return jsonify(res.json())


@main.route('/broadcast/<int:id>', methods=['POST'])
def lock_seat(id):
    url = 'http://localhost:5000/api/broadcast/' + str(id)
    info = request.json
    res = requests.post(url=url, json=info)
    return jsonify(res.json())


@main.route('/broadcast/<int:id>', methods=['DELETE'])
def unlock_seat(id):
    url = 'http://localhost:5000/api/broadcast/' + str(id)
    info = request.json
    res = requests.delete(url=url, json=info)
    return jsonify(res.json())