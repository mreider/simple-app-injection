import base64
import copy
import http
import os
import logging

import jsonpatch
from flask import Flask, jsonify, request

app = Flask(__name__)

environment_id = os.getenv("ENVIRONMENT_ID", "rss61842")
pass_token = os.getenv("DT_PAAS_TOKEN")
flavor = os.getenv("FLAVOR", "multidistro")
technology = os.getenv("TECHNOLOGY", "all")
network_zone = os.getenv("DT_NETWORK_ZONE")


def modify_pod_spec(modified_spec):
    try:
        # add volume to the pod
        modified_spec["spec"]["volumes"] = [
            {
                "name": "oneagent",
                "emptyDir": {},
            }
        ]

        # add volume mounts and env to all the containers of the customer app
        for container in modified_spec["spec"]["containers"]:
            container["volumeMounts"] = [
                {
                    "name": "oneagent",
                    "mountPath": "/opt/dynatrace/oneagent",
                }
            ]
            container["env"] = [
                {
                    "name": "LD_PRELOAD",
                    "value": "/opt/dynatrace/oneagent/agent/lib64/liboneagentproc.so"
                },
                {
                    "name": "DT_NETWORK_ZONE",
                    "value": f'{network_zone}'
                }
            ]

        # add install-oneagent init container to the pod
        modified_spec["spec"]["initContainers"] = [
            {
                "name": "install-oneagent",
                "image": "alpine:latest",
                "command": ["/bin/sh"],
                "args": [
                    "-c",
                    'ARCHIVE=$(mktemp) && wget -O $ARCHIVE "$DT_API_URL/v1/deployment/installer/agent/unix/paas/latest?Api-Token=$DT_PAAS_TOKEN&$DT_ONEAGENT_OPTIONS" && unzip -o -d /opt/dynatrace/oneagent $ARCHIVE && rm -f $ARCHIVE'
                ],
                "env": [
                    {
                        "name": "DT_API_URL",
                        "value": f'https://{environment_id}.sprint.dynatracelabs.com/api'
                    },
                    {
                        "name": "DT_PAAS_TOKEN",
                        "value": f'{pass_token}'
                    },
                    {
                        "name": "DT_ONEAGENT_OPTIONS",
                        "value": f'flavor={flavor}&include={technology}'
                    }
                ],
                "volumeMounts": [
                    {
                        "name": "oneagent",
                        "mountPath": "/opt/dynatrace/oneagent",
                    }
                ]
            }
        ]
    except KeyError:
        pass

    return modified_spec


def configure_routes(flask_app):
    @flask_app.route("/mutate", methods=["POST"])
    def mutate():
        flask_app.logger.info(f'in /mutate handler REQ: {request.json}')
        spec = request.json["request"]["object"]
        modified_spec = copy.deepcopy(spec)

        modified_spec = modify_pod_spec(modified_spec)
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

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
