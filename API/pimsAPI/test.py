import functools
from flask import Blueprint, g, redirect, request, session, url_for

from .db import get_db

bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/values')
def values():
    return 'Hello world'