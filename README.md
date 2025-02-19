# InfraFlow - Simplified Infrastructure Automation

## 🚀 Overview
InfraFlow is a **lightweight, YAML-based DSL** that simplifies Kubernetes and infrastructure automation. It enables users to define infrastructure configurations concisely while generating fully functional Ansible playbooks.

🔹 **Why InfraFlow?**
- **Compact & Readable Syntax** – Removes verbosity from traditional Ansible scripts.
- **Automation-First Approach** – Generate and execute Ansible playbooks with ease.
- **Extensible** – Easily supports new infrastructure components.
- **Kubernetes & Helm Ready** – Built-in support for k3s, Cilium, OpenTelemetry, and Jaeger.

## 🛠️ Features
✅ Declarative & YAML-based DSL for automation
✅ Converts DSL into an Ansible playbook
✅ Includes support for Helm, Firewall Rules, Kubernetes Operators
✅ Built-in verification for successful deployment

## 📜 DSL Syntax
A basic InfraFlow file looks like this:
```yaml
install:
  - k3s: curl -sfL https://get.k3s.io | sh -
  - wait: kubectl wait --for=condition=Ready node --all --timeout=60s

configure:
  kubeconfig:
    path: ~/.bashrc
    export: KUBECONFIG=/etc/rancher/k3s/k3s.yaml

firewall:
  allow:
    - { port: 6443, proto: tcp }
    - { port: 8472, proto: udp }

helm:
  check: helm version
  install: snap install helm

cilium:
  helm:
    repo: https://helm.cilium.io
    install:
      namespace: kube-system
      values:
        hubble:
          enabled: true
  wait: kubectl wait --for=condition=Ready pod -n kube-system -l k8s-app=cilium --timeout=300s
  test: cilium connectivity test

monitoring:
  OpenTelemetry: https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
  Jaeger: https://github.com/jaegertracing/jaeger-operator/releases/latest/download/jaeger-operator.yaml

verify:
  nodes: kubectl get nodes
  pods: kubectl get pods -A
```

## 🔧 Usage
### 1️⃣ Install InfraFlow
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-repo/infraflow.git
cd infraflow
pip install -r requirements.txt
```

### 2️⃣ Convert DSL to Ansible Playbook
Run the InfraFlow parser to generate an Ansible playbook:
```bash
python ifdsl_to_ansible.py example_playbook.yaml > generated_playbook.yml
```

### 3️⃣ Execute the Playbook
Run the generated Ansible playbook:
```bash
ansible-playbook -i inventory.yml generated_playbook.yml
```

## 🎯 Advantages
✅ **Simplifies Infrastructure Management**
✅ **Reduces Complexity & Redundancy**
✅ **Highly Extensible for Custom Automation Needs**
✅ **Integrates Easily with Existing Ansible Workflows**

## 📌 Contributing
We welcome contributions! Feel free to:
- Submit issues or feature requests
- Improve the documentation
- Create PRs with new functionalities

## 📝 License
InfraFlow is licensed under the **MIT License**.

🚀 **Start automating with InfraFlow today!**
