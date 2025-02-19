# Domain-Specific Language (DSL) for Infrastructure Automation

## Overview
This DSL simplifies infrastructure automation by providing a more concise and structured approach compared to traditional Ansible scripts. Unlike standard Ansible playbooks, which can become verbose and complex, this DSL abstracts repetitive tasks and enhances readability while still maintaining full automation capabilities. It is particularly beneficial for managing Kubernetes components like **k3s, Cilium, OpenTelemetry, and Jaeger**, allowing users to define infrastructure with minimal effort and maximum clarity.
This DSL is designed to define infrastructure automation tasks concisely while generating a fully functional Ansible playbook. It allows for easy installation, configuration, and verification of Kubernetes components like **k3s, Cilium, OpenTelemetry, and Jaeger**.

## Syntax and Structure
The DSL is structured using YAML syntax, breaking down the automation into key sections:

### **1. Install Section**
Used to define system-level installation commands.
```yaml
install:
  - k3s: curl -sfL https://get.k3s.io | sh -
  - wait: kubectl wait --for=condition=Ready node --all --timeout=60s
```
- **`k3s`**: Installs k3s using a shell command.
- **`wait`**: Ensures the node is ready before proceeding.

### **2. Configure Section**
Used to apply system configurations like environment variables.
```yaml
configure:
  kubeconfig:
    path: ~/.bashrc
    export: KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```
- **`kubeconfig`**: Ensures KUBECONFIG is set correctly and persists across reboots.

### **3. Firewall Section**
Defines firewall rules for allowing required ports. This section supports specifying both IP ranges and custom firewall rules beyond ports if needed, allowing for more fine-grained network access control.
Defines firewall rules for allowing required ports.
```yaml
firewall:
  allow:
    - { port: 6443, proto: tcp }
    - { port: 10250, proto: tcp }
    - { port: 2379, proto: tcp }
    - { port: 2380, proto: tcp }
    - { port: 8472, proto: udp }
    - { port: 51820, proto: udp }
    - { port: 51821, proto: udp }
```

### **4. Helm Section**
Used to manage Helm installations.
```yaml
helm:
  check: helm version
  install: snap install helm
```
- **`check`**: Verifies if Helm is already installed.
- **`install`**: Installs Helm if not present.

### **5. Cilium Section**
Defines the installation and configuration of Cilium CNI. Hubble is enabled by default to provide observability features such as network flow monitoring and security auditing. However, it can be disabled if minimal resource usage is required or if an alternative monitoring solution is in place.
Defines the installation and configuration of Cilium CNI.
```yaml
cilium:
  helm:
    repo: https://helm.cilium.io
    install:
      namespace: kube-system
      values:
        kubeProxyReplacement: true
        hubble:
          enabled: true
          relay: { enabled: true }
          ui: { enabled: true }
  wait: kubectl wait --for=condition=Ready pod -n kube-system -l k8s-app=cilium --timeout=300s
  test: cilium connectivity test
```
- **`repo`**: Specifies the Helm repository for Cilium.
- **`install`**: Installs Cilium with specific values.
- **`wait`**: Waits for Cilium to be ready.
- **`test`**: Runs a connectivity test after installation.

### **6. Monitoring Section**
Defines observability components like OpenTelemetry, Jaeger, and Hubble.
```yaml
monitoring:
  OpenTelemetry: https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
  Jaeger: https://github.com/jaegertracing/jaeger-operator/releases/latest/download/jaeger-operator.yaml
  Hubble: https://raw.githubusercontent.com/cilium/hubble/main/install/kubernetes/manifests/hubble-ui.yaml
```
- **Each key defines a monitoring tool and its respective deployment YAML file.**

### **7. Verification Section**
Defines tasks to verify system health.
```yaml
verify:
  nodes: kubectl get nodes
  pods: kubectl get pods -A
  cilium: cilium status
  jaeger: kubectl get jaeger
  opentelemetry: kubectl get otelcol
  hubble-ui: kubectl get hubble-ui
  hubble-relay: kubectl get hubble-relay
```
- **Runs various commands to verify that installed components are functional.**

## **How to Use the DSL**
This DSL is designed to be converted into an Ansible playbook using the `dsl_to_ansible.py` script. You can find the script in the official repository: [InfraFlow GitHub Repository](https://github.com/your-repo/infraflow).

1. **Write a YAML file** using this DSL structure.
2. **Run the parser** to convert it into an Ansible playbook:
   ```bash
   python dsl_to_ansible.py my_dsl.yaml > generated_playbook.yml
   ```
3. **Execute the generated playbook**:
   ```bash
   ansible-playbook -i inventory.yml generated_playbook.yml
   ```

## **Advantages of This DSL**
✅ **Compact syntax** compared to Ansible YAML.  
✅ **Easy readability** with structured automation.  
✅ **Reduces redundancy** by simplifying common tasks.  
✅ **Quickly generates playbooks** from concise definitions.  
✅ **Extensible**—new infrastructure components can be easily integrated by adding more sections to the DSL.

## **Conclusion**
This DSL provides a **concise and expressive way** to define infrastructure automation tasks. It significantly reduces verbosity while preserving all automation logic. The **DSL parser converts this format into a full Ansible playbook**, making it easy to manage Kubernetes-based deployments. 🚀

