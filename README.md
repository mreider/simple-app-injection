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