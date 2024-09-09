from bson.objectid import ObjectId
from marshmallow import Schema, fields, validate, ValidationError
from backend.extensions import mongo


class PainEntrySchema(Schema):
    user_id = fields.String(required=True)
    time_stamp = fields.DateTime(format="%Y-%m-%d %H:%M", required=True)
    strength = fields.Float(required=True, validate=validate.Range(min=1, max=3))


class PainEntry:

    def __init__(self,
                 user_id,
                 time_stamp,
                 strength,
                 location,
                 submit_time):
        self.user_id = user_id
        self.time_stamp = time_stamp
        self.strength = strength
        self.location = location
        self.submit_time = submit_time

    def save(self):
        result = mongo.db.painEntries.find_one({
            "user_id": self.user_id,
            "time_stamp": self.time_stamp
        })
        if result:
            # wrong method called, use update instead
            raise ValueError("Wrong Method called, use update instead")
        
        return mongo.db.painEntries.insert_one({
            "user_id": self.user_id,
            "time_stamp": self.time_stamp,
            "strength": self.strength,
            "location": self.location,
            "submit_time": self.submit_time
        }).inserted_id
