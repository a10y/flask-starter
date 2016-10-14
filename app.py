"""
Simple flask starter application
"""
from flask import Flask, jsonify, request, Response

from functools import wraps

##################################################
# Decorators
##################################################

def response_json(f):
    """
    Marks that the method returns a JSON response.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        result = f(*args, **kwargs)
        return jsonify(result)
    return wrapped

def get(route):
    return app.route(route, methods=['GET'])

def post(route):
    return app.route(route, methods=['POST'])

def put(route):
    return app.route(route, methods=['PUT'])

def delete(route):
    return app.route(route, methods=['DELETE'])


###########################
# Main logic
###########################

app = Flask(__name__)

db = dict() # database!

###########################
# Routes
###########################


@get("/db/<path:key>")
@response_json
def lookup(key):
    app.logger.debug('searching for key={} in {}'.format(key, db))
    return db.get(key, dict(success=False))

@post("/db/<path:key>")
@response_json
def insert(key):
    value = request.get_json()['value']
    app.logger.debug("inserting {} -> {}".format(key, value))
    db[key] = value
    app.logger.debug('inserted. db={}'.format(db))
    return dict(success=True)

@delete("/db/<path:key>")
@response_json
def remove(key):
    if key in db:
        del db[key]
    return dict(success=True)

###########################
# Start
###########################

# Listen....can you hear it?
app.run(debug=True, host='0.0.0.0')

