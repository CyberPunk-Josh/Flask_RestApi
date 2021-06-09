from flask_restful import Resource, reqparse
from models.users import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be blank'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be blank'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        # model find by name
        if UserModel.find_by_username(data['username']):
            return{'message': 'User already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    parser = reqparse.RequestParser()

    def get(self, username):
        user = UserModel.find_by_name(username)
        if user:
            return {"message": "User en la bd"}
        return {'message': 'User no encontrado'}, 404
