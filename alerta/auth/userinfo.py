
import re

from flask import request, jsonify
from flask_cors import cross_origin

from alerta.exceptions import ApiError
from alerta.auth.utils import permission
from alerta.models.token import Jwt
from . import auth


@auth.route('/userinfo', methods=['OPTIONS', 'GET'])
@cross_origin()
@permission('read:userinfo')
def userinfo():
    auth_header = request.headers.get('Authorization', '')
    m = re.match(r'Bearer (\S+)', auth_header)
    token = m.group(1) if m else None

    if token:
        return jsonify(Jwt.parse(token).serialize)
    else:
        raise ApiError('Missing authorization Bearer token', 401)
