from src.app import modify_pod_spec
import unittest
from flask import Flask
from src.app import configure_routes


json_request = {
    'kind': 'AdmissionReview', 'apiVersion': 'admission.k8s.io/v1',
    'request': {'uid': '73d914d3-c856-4042-9eae-eead6742a137',
                'kind': {'group': '', 'version': 'v1', 'kind': 'Pod'},
                'resource': {'group': '', 'version': 'v1', 'resource': 'pods'},
                'requestKind': {'group': '', 'version': 'v1', 'kind': 'Pod'},
                'requestResource': {'group': '', 'version': 'v1', 'resource': 'pods'}, 'name': 'nginx',
                'namespace': 'test', 'operation': 'CREATE',
                'userInfo': {'username': 'minikube-user', 'groups': ['system:masters', 'system:authenticated']},
                'object': {'kind': 'Pod', 'apiVersion': 'v1',
                           'metadata': {'name': 'nginx', 'namespace': 'test', 'creationTimestamp': None,
                                        'labels': {'run': 'nginx'}, 'annotations': {
                                   'kubectl.kubernetes.io/last-applied-configuration': '{"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"creationTimestamp":null,"labels":{"run":"nginx"},"name":"nginx","namespace":"test"},"spec":{"containers":[{"image":"nginx","name":"nginx","resources":{}}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always"},"status":{}}\n'},
                                        'managedFields': [
                                            {'manager': 'kubectl-client-side-apply', 'operation': 'Update',
                                             'apiVersion': 'v1', 'time': '2022-10-22T12:08:11Z',
                                             'fieldsType': 'FieldsV1', 'fieldsV1': {'f:metadata': {
                                                'f:annotations': {'.': {},
                                                                  'f:kubectl.kubernetes.io/last-applied-configuration': {}},
                                                'f:labels': {'.': {}, 'f:run': {}}}, 'f:spec': {'f:containers': {
                                                'k:{"name":"nginx"}': {'.': {}, 'f:image': {},
                                                                       'f:imagePullPolicy': {}, 'f:name': {},
                                                                       'f:resources': {},
                                                                       'f:terminationMessagePath': {},
                                                                       'f:terminationMessagePolicy': {}}},
                                                'f:dnsPolicy': {},
                                                'f:enableServiceLinks': {},
                                                'f:restartPolicy': {},
                                                'f:schedulerName': {},
                                                'f:securityContext': {},
                                                'f:terminationGracePeriodSeconds': {}}}}]},
                           'spec': {'volumes': [{'name': 'kube-api-access-66f7j', 'projected': {
                               'sources': [{'serviceAccountToken': {'expirationSeconds': 3607, 'path': 'token'}}, {
                                   'configMap': {'name': 'kube-root-ca.crt',
                                                 'items': [{'key': 'ca.crt', 'path': 'ca.crt'}]}}, {'downwardAPI': {
                                   'items': [{'path': 'namespace', 'fieldRef': {'apiVersion': 'v1',
                                                                                'fieldPath': 'metadata.namespace'}}]}}],
                               'defaultMode': 420}}], 'containers': [
                               {'name': 'nginx', 'image': 'nginx', 'resources': {}, 'volumeMounts': [
                                   {'name': 'kube-api-access-66f7j', 'readOnly': True,
                                    'mountPath': '/var/run/secrets/kubernetes.io/serviceaccount'}],
                                'terminationMessagePath': '/dev/termination-log',
                                'terminationMessagePolicy': 'File', 'imagePullPolicy': 'Always'}],
                                    'restartPolicy': 'Always', 'terminationGracePeriodSeconds': 30,
                                    'dnsPolicy': 'ClusterFirst', 'serviceAccountName': 'default',
                                    'serviceAccount': 'default', 'securityContext': {},
                                    'schedulerName': 'default-scheduler', 'tolerations': [
                                   {'key': 'node.kubernetes.io/not-ready', 'operator': 'Exists',
                                    'effect': 'NoExecute', 'tolerationSeconds': 300},
                                   {'key': 'node.kubernetes.io/unreachable', 'operator': 'Exists',
                                    'effect': 'NoExecute', 'tolerationSeconds': 300}], 'priority': 0,
                                    'enableServiceLinks': True, 'preemptionPolicy': 'PreemptLowerPriority'},
                           'status': {}}, 'oldObject': None, 'dryRun': False,
                'options': {'kind': 'CreateOptions', 'apiVersion': 'meta.k8s.io/v1',
                            'fieldManager': 'kubectl-client-side-apply'}}
}

pod_spec = {'kind': 'Pod', 'apiVersion': 'v1',
            'metadata': {'name': 'nginx', 'namespace': 'test', 'creationTimestamp': None,
                         'labels': {'run': 'nginx'}, 'annotations': {
                    'kubectl.kubernetes.io/last-applied-configuration': '{"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"creationTimestamp":null,"labels":{"run":"nginx"},"name":"nginx","namespace":"test"},"spec":{"containers":[{"image":"nginx","name":"nginx","resources":{}}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always"},"status":{}}\n'},
                         'managedFields': [
                             {'manager': 'kubectl-client-side-apply', 'operation': 'Update',
                              'apiVersion': 'v1', 'time': '2022-10-22T12:08:11Z',
                              'fieldsType': 'FieldsV1', 'fieldsV1': {'f:metadata': {
                                 'f:annotations': {'.': {},
                                                   'f:kubectl.kubernetes.io/last-applied-configuration': {}},
                                 'f:labels': {'.': {}, 'f:run': {}}}, 'f:spec': {'f:containers': {
                                 'k:{"name":"nginx"}': {'.': {}, 'f:image': {},
                                                        'f:imagePullPolicy': {}, 'f:name': {},
                                                        'f:resources': {},
                                                        'f:terminationMessagePath': {},
                                                        'f:terminationMessagePolicy': {}}},
                                 'f:dnsPolicy': {},
                                 'f:enableServiceLinks': {},
                                 'f:restartPolicy': {},
                                 'f:schedulerName': {},
                                 'f:securityContext': {},
                                 'f:terminationGracePeriodSeconds': {}}}}]},
            'spec': {'volumes': [{'name': 'kube-api-access-66f7j', 'projected': {
                'sources': [{'serviceAccountToken': {'expirationSeconds': 3607, 'path': 'token'}}, {
                    'configMap': {'name': 'kube-root-ca.crt',
                                  'items': [{'key': 'ca.crt', 'path': 'ca.crt'}]}}, {'downwardAPI': {
                    'items': [{'path': 'namespace', 'fieldRef': {'apiVersion': 'v1',
                                                                 'fieldPath': 'metadata.namespace'}}]}}],
                'defaultMode': 420}}], 'containers': [
                {'name': 'nginx', 'image': 'nginx', 'resources': {}, 'volumeMounts': [
                    {'name': 'kube-api-access-66f7j', 'readOnly': True,
                     'mountPath': '/var/run/secrets/kubernetes.io/serviceaccount'}],
                 'terminationMessagePath': '/dev/termination-log',
                 'terminationMessagePolicy': 'File', 'imagePullPolicy': 'Always'}],
                     'restartPolicy': 'Always', 'terminationGracePeriodSeconds': 30,
                     'dnsPolicy': 'ClusterFirst', 'serviceAccountName': 'default',
                     'serviceAccount': 'default', 'securityContext': {},
                     'schedulerName': 'default-scheduler', 'tolerations': [
                    {'key': 'node.kubernetes.io/not-ready', 'operator': 'Exists',
                     'effect': 'NoExecute', 'tolerationSeconds': 300},
                    {'key': 'node.kubernetes.io/unreachable', 'operator': 'Exists',
                     'effect': 'NoExecute', 'tolerationSeconds': 300}], 'priority': 0,
                     'enableServiceLinks': True, 'preemptionPolicy': 'PreemptLowerPriority'},
            'status': {}}


def get_client():
    app = Flask(__name__)
    configure_routes(app)
    return app.test_client()


class TestMutate(unittest.TestCase):
    def setUp(self) -> None:
        self.client = get_client()

    def test_health_route(self):
        url = '/health'
        response = self.client.get(url)

        assert response.status_code == 204

    def test_mutate_without_init_containers(self):
        got_spec = modify_pod_spec(pod_spec)

        assert len(got_spec["spec"]["initContainers"]) == 1
        assert len(got_spec["spec"]["volumes"]) == 1
        assert len(got_spec["spec"]["containers"][0]["volumeMounts"]) == 1

    def test_mutate_base_response(self):
        url = '/mutate'
        response = self.client.post(url, json=json_request)

        assert response.status_code == 200
        assert response.json["kind"] == "AdmissionReview"
        assert response.json["apiVersion"] == "admission.k8s.io/v1"
        assert response.json["response"]["allowed"] is True
        assert response.json["response"]["patchType"] == "JSONPatch"
        assert response.json["response"]["uid"] == "73d914d3-c856-4042-9eae-eead6742a137"
