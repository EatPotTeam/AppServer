from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication
from . import orders
from . import coupons