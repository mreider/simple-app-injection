# simple-app-injection
A simple way of injecting Dynatrace code modules into pods

# WORK IN PROGRESS - NONFUNCTIONAL

# Getting started

Begin by deploying the mdr-webhook app

`kubectl apply -f k8s/deployment.yaml`

Next deploy the admission controller

`kubectl apply -f k8s/mutate.yaml`

Now create certificates for everything

`kubectl apply -f cert-manager-job.yaml`

---

# Getting started

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

```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/mutating-webhook.yaml
```


It is possible to run the mutating webhook locally on [minikube](https://minikube.sigs.k8s.io/docs/start/) k8s cluster

To do: rebuild the docker image