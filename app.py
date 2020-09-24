from flask import Flask
from flask_restful import Api

from infrastructure import repository
from resources.documents import Documents

repository.create_all()

app = Flask(__name__)
api = Api(app)

api.add_resource(
    Documents,
    '/documents',
    '/documents/<string:title>',
    '/documents/<string:title>/<string:latest>',
    '/documents/<string:title>/<string:timestamp>',
)


if __name__ == '__main__':
    app.run(debug=True)
