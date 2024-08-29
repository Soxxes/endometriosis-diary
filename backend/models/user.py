from bson.objectid import ObjectId
from passlib.hash import sha256_crypt
from marshmallow import Schema, fields, validate, ValidationError
from backend.extensions import mongo


class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    height = fields.Float(required=True, validate=validate.Range(min=0))
    weight = fields.Float(required=True, validate=validate.Range(min=0))
    # TODO: make date field
    birthday = fields.String(required=True)

user_schema = UserSchema()


class User:

    def __init__(self,
                 username,
                 email,
                 password,
                 height,
                 weight,
                 birthday):
        self.username = username
        self.email = email
        self.password = password
        self.height = height
        self.weight = weight
        # for age specific data analytics
        self.birthday = birthday

    def save(self):
        return mongo.db.users.insert_one({
            "name": self.username,
            "email": self.email,
            "password": sha256_crypt.encrypt(self.password),
            # TODO: encrypt ? since sensitive information
            "height": self.height,
            "weight": self.weight,
            "birthday": self.birthday
        }).inserted_id
    
    @staticmethod
    def get_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def update(user_id, data):
        return mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})

    @staticmethod
    def delete(user_id):
        return mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def validate(data):
        try:
            validated_data = user_schema.load(data)
            return validated_data, None
        except ValidationError as err:
            return None, err.messages

