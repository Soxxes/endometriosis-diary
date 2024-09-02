from bson.objectid import ObjectId
from marshmallow import Schema, fields, validate, ValidationError
from backend.extensions import mongo


class FoodEntrySchema(Schema):
    user_id = fields.String(required=True)
    # a list of consumed foods organized in a list
    # ["apple", "milk"]
    foods = fields.List(cls_or_instance=fields.String, required=True)
    portion_sizes = fields.List(cls_or_instance=fields.Float, required=True)
    # liquids = fields.Float(required=True, validate=validate.Range(min=0, max=10))
    alcohol = fields.Boolean(required=True)
    # describes the activity level of that day
    activity = fields.Float(required=True, validate=validate.Range(min=0, max=3))
    fast_food = fields.Boolean(required=True)
    date = fields.DateTime(format="%Y-%m-%d", required=True)
    # when the foods in field "foods" were consumed
    # example:
    # DateTime(2024, 9, 2, 9, 0)
    meal_time_stamp = fields.DateTime(format="%Y-%m-%d %H:%M", required=True)
    nutritions = fields.Dict(keys=fields.String, values=fields.Float, required=True)
    submit_time = fields.DateTime(format="%Y-%m-%d %H:%M", required=True)

food_entry_schema = FoodEntrySchema()


class FoodEntry:

    def __init__(self,
                 user_id,
                 foods,
                 portion_sizes,
                #  liquids,
                 alcohol,
                 activity,
                 fast_food,
                 date,
                 meal_time_stamp,
                 nutritions,
                 submit_time):
        self.user_id = user_id
        self.foods = foods
        self.portion_sizes = portion_sizes
        # self.liquids = liquids
        self.alcohol = alcohol
        self.activity = activity
        self.fast_food = fast_food
        self.date = date
        self.meal_time_stamp = meal_time_stamp
        self.nutritions = nutritions
        self.submit_time =submit_time

    def save(self):
        result = mongo.db.foodEntries.find_one({
            "user_id": self.user_id,
            "meal_time_stamp": self.meal_time_stamp
        })
        if result:
            # wrong method called, use update instead
            raise ValueError("Wrong Method called, use update instead")
        
        return mongo.db.foodEntries.insert_one({
            "user_id": self.user_id,
            "foods": self.foods,
            "portion_sizes": self.portion_sizes,
            # "liquids": self.liquids,
            "alcohol": self.alcohol,
            "activity": self.activity,
            "fast_food": self.fast_food,
            "date": self.date,
            "meal_time_stamps": self.meal_time_stamp,
            "nutritions": self.nutritions,
            "submit_time": self.submit_time
        }).inserted_id
    
    @staticmethod
    def get_by_id(foodEntry_id):
        return mongo.db.foodEntries.find_one({"_id": ObjectId(foodEntry_id)})

    @staticmethod
    def get_by_user_and_meal_time_stamp(user_id, meal_time_stamp):
        return mongo.db.foodEntries.find_one({
            "user_id": user_id,
            "meal_time_stamp": meal_time_stamp
        })

    @staticmethod
    def update(foodEntry_id, data):
        return mongo.db.foodEntries.update_one({"_id": ObjectId(foodEntry_id)}, {"$set": data})

    @staticmethod
    def delete(foodEntry_id):
        return mongo.db.foodEntries.delete_one({"_id": ObjectId(foodEntry_id)})
    
    @staticmethod
    def validate(data):
        try:
            validated_data = food_entry_schema.load(data)
            return validated_data, None
        except ValidationError as err:
            return None, err.messages
