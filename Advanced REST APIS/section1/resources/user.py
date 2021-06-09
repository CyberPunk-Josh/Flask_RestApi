from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

BLANK_ERROR = 'This field cannot be blank'
USERNAME_EXISTS = "A user with that username already exists"
USER_CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = 'User not found'
USER_DELETED = 'User deleted'
INVALID_CREDENTIALS = 'Invalid Credentials'
SUCCESSFULLY_LOG_OUT = 'Successfully Log Out!'


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help=BLANK_ERROR
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help=BLANK_ERROR
                        )

    @classmethod
    def post(cls):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": USERNAME_EXISTS}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": USER_CREATED_SUCCESSFULLY}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 400
        user.delete_from_db()
        return {'message': USER_DELETED}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help=BLANK_ERROR
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help=BLANK_ERROR
                        )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {'message': INVALID_CREDENTIALS}


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {'message': SUCCESSFULLY_LOG_OUT}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        return {'access_token': new_token}
