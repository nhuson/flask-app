from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime
from src.configs import Config

def authenicate_required():
  def _authenicate(f):
    @wraps(f)
    def __authenicate(*args, **kwargs):
      jwtToken = request.headers.get('x-access-token')
      if jwtToken is None:
        return jsonify({"success": False, "message": "Missing token on request."}), 400
      if jwtToken != Config.PRIVATE_TOKEN_VADDRESS:
        return jsonify({"success": False, "message": "Incorrect token."}), 400

      return f(*args, **kwargs)
    return __authenicate
  return _authenicate