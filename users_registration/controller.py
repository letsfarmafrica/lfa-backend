from pymongo import MongoClient
from urllib.parse import quote_plus
import bcrypt

from users_registration import config

class Controller:
    """
    a controller class that handles users registration, login
    logout, initiation of password reset and finalization of password reset.
    """

    def __init__(self):
        self.logged_in = False
        uri = "mongodb://%s:%s@%s" % (quote_plus(config.DB_ROOT), quote_plus(config.DB_USERNAME), config.DB_HOST)
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            self.db = self.client[config.DB_NAME]
            self.collection = self.db[config.DB_COLLECTION]
        except Exception as e:
            print(e.message)

    def create_user(self, database, user, password):
        database.command('createUser', user, pwd=password, roles=['readWrite'])

    def register(self, newUser):
        old_user = self.collection.find_one({'email': newUser.email})

        if old_user is not None:
            raise(Exception)
        else:
            # create hash of the new password
            bytes = newUser.password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt)

            new_user = {
                'email': newUser.email,
                'password': hash,
                'polygon': newUser.polygon
            }
            self.collection.insert_one(new_user)

    def login(self, user):
        existing_user = self.collection.find_one({'email': user.email})

        if existing_user is None:
            # raise(Exception)
            self.register(user)
            return True

        else:
            user_password = user['password'].encode('utf-8')
            correct_password = bcrypt.checkpw(user_password, existing_user.password)
            if correct_password:
                self.logged_in = True
                return True
            else:
                #TODO: return a response that the password is not correct.
                raise(Exception)

    def log_off(self):
        self.logged_in = False

    def password_reset(self, new_password, email):
        bytes = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)

        new_values = {"$set": {'password': hash}}

        self.collection.update_one({'email': email}, new_values)

    def get_user_by_email(self, email):
        user_object = self.collection.find_one({'email': email})
        return user_object

    def update_geometry(self, polygon, email):
        new_values = {"$set": {'polygon': polygon}}

        self.collection.update_one({'email': email}, new_values)

    def update_history(self, user_object, items):

        products_bucket_list = user_object.products_bucket_list

        if (products_bucket_list is not None
            and isinstance(products_bucket_list, list)
            and len(products_bucket_list) > 0):
            for key, item in items:
                if item['identifier'] not in products_bucket_list:
                    products_bucket_list.append(item['identifier'])

        last_product_date = user_object.last_product_date

        new_values = {
            "$set": {
                'products_bucket_list': products_bucket_list,
                'last_product_date': last_product_date
            }
        }

        self.collection.update_one({'email': user_object.email}, new_values)

    def get_users(self):
        users = []
        items = self.collection.find()
        for item in items:
            users.append(item['email'])
        return users
