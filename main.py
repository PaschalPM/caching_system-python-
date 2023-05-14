#!/home/pasmac/.local/share/virtualenvs/caching_tuts-9vgzpVHR/bin/python3
from models.schema.user import User
from flask import Flask, jsonify, request as req
from models.user import User
from storage.cache import Cache
from requests import request as server_req

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/users')
def users_view():
    
    # With Caching
    # return jsonify(Cache.DBResource(req.path, User.all))

    # Without Caching
    return jsonify(User.all())

@app.route('/users/<int:id>')
def user_view(id):
    # With Caching
    # return jsonify(Cache.DBResource(req.path, lambda : User.get(id)))

    # Without Caching
    return (User.get(id))

EXT_USERS_URL = 'https://jsonplaceholder.typicode.com/users?_embed=todos'
def getUsers(id=''):
        return server_req('get', EXT_USERS_URL+'/'+str(id))
    
@app.route('/ext/users')
def ext_users_view():
        
    # With caching
    # return jsonify(Cache.ExtResource(req.path, getUsers))

    # Without Caching
    if getUsers().status_code == 200:
        return jsonify(getUsers().json())
    

@app.route('/ext/users/<int:id>')
def ext_user_view(id):
    
    # With caching
    # user_res_obj = lambda : getUsers(id)
    # return jsonify(Cache.ExtResource(req.path, user_res_obj))

    # Without Caching
    if getUsers(id).status_code == 200:
        return jsonify(getUsers(id).json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

