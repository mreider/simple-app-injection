import base64
import copy
import http
import json
import random
import logging

import jsonpatch
from flask import Flask, jsonify, request

app = Flask(__name__)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def configure_routes(flask_app):
    @flask_app.route("/mutate", methods=["POST"])
    def mutate():
        flask_app.logger.info(f'in /mutate handler REQ: {request.json}')
        spec = request.json["request"]["object"]
        modified_spec = copy.deepcopy(spec)

        try:
            modified_spec["metadata"]["labels"]["run"] = "kitty"
        except KeyError:
            pass
        patch = jsonpatch.JsonPatch.from_diff(spec, modified_spec)

        temp = {
                "apiVersion": "admission.k8s.io/v1",
                "kind": "AdmissionReview",
                "response": {
                    "allowed": True,
                    "uid": request.json["request"]["uid"],
                    "patch": base64.b64encode(str(patch).encode()).decode(),
                    "patchType": "JSONPatch",
                }
            }
        flask_app.logger.debug(f'in /mutate handler RES: {temp}')

        return jsonify(temp)

    @flask_app.route("/health", methods=["GET"])
    def health():
        return "", http.HTTPStatus.NO_CONTENT


configure_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
