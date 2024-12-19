# GCP PLAYGROUND

## Build out GCP instance and SSH

terraform apply
g compute instances list
g compute ssh kubernetes-playground

## Install Docker and Minikube

sudo apt-get update -y
sudo apt install docker.io
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
sudo usermod -aG docker $USER && newgrp docker
minikube start --driver=docker

