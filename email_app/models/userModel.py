from email_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('email_validation_schema').query_db(query)

        users = []

        for user in results:
            users.append(cls(user))

        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        return connectToMySQL('email_validation_schema').query_db(query, data)

    @classmethod
    def findUserByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('email_validation_schema').query_db(query, data)

        user = None

        if results:
            print(results)
            if len(results) > 0:
                user = cls(results[0])

        return user

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(userId)s"
        return connectToMySQL('email_validation_schema').query_db(query, data)

    @staticmethod
    def validateUser(user):
        is_valid = True

        email = user['email']

        if not EMAIL_REGEX.match(email):
            flash('Invalid email address!', 'error')
            is_valid = False
        
        if User.findUserByEmail({'email': email}) != None:
            flash('Email address is already taken!', 'error')
            is_valid = False

        if is_valid:
            flash(f'The email address you entered ({email}) is a VALID email address! Thank you!', 'success')

        return is_valid