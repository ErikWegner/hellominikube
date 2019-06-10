Hello World on Minikube
=======================

This repository contains a very simple http server [in python](server.py) packaged as a [Docker](Dockerfile) container.

The container is deployed to a local minikube for educational purposed.

This version uses [nginx](https://kubernetes.github.io/ingress-nginx/) as ingress controller. For an alternative with traefik, see [this branch](https://github.com/ErikWegner/hellominikube/tree/traefik).

Minikube deployment
------------------

1. Download and start [minikube](https://kubernetes.io/de/docs/setup/minikube/).
2. Enable default nginx [ingress controller](https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/) basically by running `minikube addons enable ingress`.
3. Deploy the container: `kubectl apply -f deployment.yaml`.
4. Create a service: `kubectl apply -f service.yaml`.
5. Provide an ingress for the service: `kubectl apply -f ingress.yaml`.
6. Connect to the minikube deployment, e. g. https://192.168.99.100/hellominikube/it-works/
