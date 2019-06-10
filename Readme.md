Hello World on Minikube
=======================

This repository contains a very simple http server [in python](server.py) packaged as a [Docker](Dockerfile) container.

The container is deployed to a local minikube for educational purposed.

This version uses [Traefik](https://docs.traefik.io/user-guide/kubernetes/) as ingress controller. For an alternative with nginx, see [this branch](https://github.com/ErikWegner/hellominikube/tree/master).

Minikube deployment
------------------

1. Download and start [minikube](https://kubernetes.io/de/docs/setup/minikube/).
2. Disable default nginx ingress controller by running `minikube addons disable ingress`.
3. Regenerate certificate: `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=traefik-ui.minikube"`
4. Save certifiate as kubernetes secret: `kubectl create secret generic traefik-cert --from-file=tls.crt --from-file=tls.key --namespace kube-system`
5. Deploy the traefik ingress controller: `kubectl apply -f traefik.yaml`
4. Regenerate certificate
4. Deploy the container: `kubectl apply -f deployment.yaml`.
5. Create a service: `kubectl apply -f service.yaml`.
6. Provide an ingress for the service: `kubectl apply -f ingress.yaml`.
7. Connect to the minikube deployment, e. g. https://192.168.99.100/hellominikube/it-works/

