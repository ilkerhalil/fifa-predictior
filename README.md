# FIFA PREDICTIOR



## Install Requirements

* [GNU Make](https://www.gnu.org/software/make/manual/make.html)

* [Docker](https://www.docker.com/)

* [Kubernetes](https://kubernetes.io/)

* [Kubeflow](https://www.kubeflow.org/)

* [Python](https://www.python.org/)

### Install Make

```sh
apt update && apt install make
```

### Install Docker

```sh
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Manage Docker as a non-root user
```sh
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```
* Please check Docker documention
 [Docker Linux Postinstall ](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)


### Install Kubectl

```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
mv kubectl /usr/local/bin
```
* Check installation

```sh
kubectl version
```

### Install MicroK8S

```sh
sudo snap install microk8s --classic
microk8s enable dns
microk8s enable dashboard
microk8s enable storage
microk8s enable cert-manager
```

* Set config for kubernetes

```sh
microk8s config > .kube/config
```

* Check microk8s installation

```sh
kubectl get nodes
```

## Install Kubeflow

### Install kustomize
```sh
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash
chmod +x ./kustomize
sudo mv kustomize /usr/local/bin
```

### Install kubeflow
```sh
git clone https://github.com/kubeflow/manifests.git
git checkout v1.8.0 #Checkoput v1.8.0 version for kubeflow
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
```
* Please check installation kubeflow for documention [Kubeflow Manifest](https://github.com/kubeflow/manifests)

### Install Python && SetUp pyenv

``` sh
curl https://pyenv.run | bash
```


Add those commands below to your shell

```
export PYENV_ROOT="$HOME/.pyenv
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

###  Set up python with pyenv

Python version will be specified with ".python_env" file in current directory

```
pyenv install
```

### Instructions

Set up venv for Python in the current directory

```sh
python3 -m venv .venv
source .venv/bin/activate
```

### Install Python Requirements

```sh
pip install -r dev_requirements.txt
pip install -r requirements.txt
```

### Format code

```sh
make format
```

### Lint Code

```sh
make lint
```
### Create Model

```sh
make create_model
```

### Port-Forward Kubernetes for local

```sh
kubectl port-forward svc/istio-ingressgateway -n istio-system --address 0.0.0.0 8080:80 &
```

### Deploy Kubeflow

Tag for model. Pass make KF_PIPELINES_ENDPOINT and MODEL_OUTPUT_PATH environment

```sh
make kfp-compile TAG=1.2.4 KF_PIPELINES_ENDPOINT="http://localhost:8080"  MODEL_OUTPUT_PATH="/data"
```

### Call Model

```sh
make call-model
```

## Acknowledgements

* [Python](https://www.python.org/)

* [GNU Make](https://www.gnu.org/software/make/manual/make.html)

* [Tensorflow](https://www.tensorflow.org/)

* [Docker](https://www.docker.com/)

* [Kubernetes](https://kubernetes.io/)

* [Kubeflow](https://www.kubeflow.org/)

* [KServe](https://kserve.github.io/)


