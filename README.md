# simple-app-injection
A simple way of injecting Dynatrace code modules into pods

# WORK IN PROGRESS - NONFUNCTIONAL

# Getting started

It is possible to setup the mutating webhook locally on [minikube](https://minikube.sigs.k8s.io/docs/start/) k8s cluster

Begin by installing the [cert-manager](https://cert-manager.io/docs/installation/) 

```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.10.0/cert-manager.yaml
```

Next, we create the Issuer and Certificate, which will create self-signed certificates as a secret, which will be later used by our mutating webhook:

```
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/issuer-certificate.yaml
kubectl apply -f k8s/mutating-webhook-rbac.yaml
```

Create the secrets that is later required by the deployment

```
kubectl create secret generic dynatrace-secret --from-literal DT_PAAS_TOKEN=<dt-pass-token> -n mdr-webhook
```

```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/mutating-webhook.yaml
```

To test if the mutating webhook is working as expected:

```
# create a new namespace with label => "mutate: apply"
kubectl create ns test
kubectl label namespaces test mutate=allow

kubectl apply -f k8s/test/nginx.yaml

kubectl logs -f nginx -c install-oneagent -n test           
```

### To Do

- Rebuild the docker image and push to your dockerhub, and also change the image in `k8s/deployment.yaml`
- Add a valid network zone environment value in `k8s/deployment.yaml`
