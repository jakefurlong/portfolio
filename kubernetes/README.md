# Kubernetes

Daily Warmup

- Get the status of the nodes
  - `kubectl get nodes`
- Determine the number of running pods in all namespaces
  - `kubectl get poods -A`
- Determine the number of deployments in all namespaces
  - `kubectl get deployments -A`
- Determine the number of services in all namespaces
  - `kubectl get svc -A`

Pods and Deployments

- Create a pod using the CLI / list pods after
  - `kubectl run nginx --image=nginx`
  - `kubectl get pods`
- Delete pod using the CLI / list pods after
  - `kubectl delete pod nginx`
  - `kubectl get pods`
- Create an nginx deployment using the CLI / list deployments and replicasets
  - `kubectl create deployment webapp --image=nginx`
  - `kubectl get deployments`
  - `kubectl get replicasets`
- Edit deployment and change the replicas to 2 / list pods and replicasets
  - `kubectl edit deployment webapp` (change replicas to 2)
  - `kubectl get pods`
  - `kubectl get replciasets`
- Delete deployment / list deployments after
  - `kubectl delete deployment webapp`
  - `kubectl get deployments`
- Create a postgres deployment and check the logs / log in to container and list the files
  - `kubectl create deployment postgres --image=postgress`
  - `kubectl get pods`
  - `kubectl logs <container_id>`
  - `kubectl exec -it postgres -- bash` (once inside, `ls`)
- Delete all deployments
  - `kubectl delete deployment postgres`
- Create a basic nginx deployment file and deploy an nginx pod / list pods / make change to replicas / list pods
- Delete all resources to clean up
  - `kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deployment.yaml`
  - `kubectl apply -f deployment.yaml`
  - `kubectl get pods`
  - Edit file replicas value, then `kubectl apply -f deployment.yaml`
  - `kubectl get pods`

## Components

Nodes and Pods

- A node is a server or virtual machine
- A pod is the smallest unit of kubernetes
- A pod is an abstraction over a container
- There is usually 1 application per pod
- Each pod gets its own IP address (internal)
- Pod components are ephemeral
- When a pod dies it's assigned a new IP address
- Service is a permanenet IP address that can be attached to each pod
- Lifecycle of service and pod are not connected
- External service opens communication from the Internet
- Internal services are used for private comms
- Ingress does forwarding to the service

ConfigMap and Secrets

- ConfigMap is the external configuration of your application (i.e. DB URL)
- Don't put credentials in a ConfigMap, use a Secret
- Secret is just like a ConfigMap but it's not stored in plain text

Volumes

- Storage can be local or remote
- Volumes makes data persistent
- K8S doesn't manage data persistence

Deployment and StatefulSet

- Replicas are connected to the same service
- Service is also a load balancer
- Deployment is a blueprint for pods
- Deployment is an abstraction on top of pods
- StatefulSet is meant for apps like DBs
- Apps like DBs should be created with StatefulSets
- StatefulSet is used for data consistency

## Architecture

- Each node has multiple pods running on it
- Each node has 3 processes running on it that are used to manage and schedule pods
  - Container runtime (like Docker)
  - Kubelet - interface with container runtime and the node
  - Kube-proxy - forwards the requests
- Worker nodes do the actual work
- Every master node has 4 processes running inside
  - Api Server - like a cluster gateway and acts as a gatekeeper for authentication
  - Scheduler - decides what worker node the pod will run on
    - The Kubelet acutlaly starts the pod on the node, the scheduler just schedules it
  - Controller manager - detects cluster state changes
  - etcd - key value state of a cluster state (cluster brain), every change get stored here
  - Generally speaker, master nodes need less server resources than worker nodes
  - It's recommended to have mlutiple master nodes
  
##