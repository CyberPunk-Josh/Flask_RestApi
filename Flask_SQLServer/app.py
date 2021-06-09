from flask import Flask
from flask_restful import Api
from db import db

from resources.users import UserRegister

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://server/table?driver=ODBC Driver 17 for " \
                                        "SQL Server?trusted_connection=yes "
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'joshue'
api = Api(app)

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
