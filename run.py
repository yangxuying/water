from flask import render_template, request, jsonify
from app_v1 import init_app
from flask_swagger import swagger
from flask_cors import CORS

app = init_app()
CORS(app, supports_credentials=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/config", methods=["GET", "POST"])
def config():
    return jsonify({"api": "http://{}".format(app.config.get('SERVER_NAME'))})


@app.route("/spec", methods=["GET", "POST"])
def swag_spec():
    return jsonify(swagger(app, from_file_keyword='swagger_from_file'))


@app.route("/swagger", methods=["GET"])
def swag_index():
    return render_template('swagger/index.html', data={'url': 'http://{}/spec'.format(app.config.get('SERVER_NAME'))})


if __name__ == '__main__':
    app.run()
