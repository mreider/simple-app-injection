import base64
import copy
import http
import json
import random
import logging

import jsonpatch
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/mutate", methods=["POST"])
def mutate():
    spec = request.json["request"]["object"]
    modified_spec = copy.deepcopy(spec)
    app.logger.debug('in /mutate handler')

    try:
        modified_spec["metadata"]["labels"]["run"] = "kitty"
    except KeyError:
        pass
    patch = jsonpatch.JsonPatch.from_diff(spec, modified_spec)

    app.logger.debug("## patched object:: ", patch)
    
    temp = jsonify(
        {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": True,
                "uid": request.json["request"]["uid"],
                "patch": base64.b64encode(str(patch).encode()).decode(),
                "patchtype": "JSONPatch",
            }
        }
    )
    print("## response payload::  ", temp)

    return temp


@app.route("/health", methods=["GET"])
def health():
    return ("", http.HTTPStatus.NO_CONTENT)


if __name__ == "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(host="0.0.0.0", debug=True, ssl_context='adhoc')  # pragma: no cover