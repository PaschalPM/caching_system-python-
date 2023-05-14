from . import db
from .schema.user import User as UserSchema

class User:
    @staticmethod
    def all():
     
        users = [{
            'id': user.id,
            'name': user.name,
            'phone': user.phone,
            'email': user.email
        } for user in db.all(UserSchema)]
        return (users)
    
    @staticmethod
    def get(id):
        return db.get(UserSchema, id).to_dict()