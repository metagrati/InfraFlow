import yaml
import sys

def parse_dsl(dsl_file):
    """Reads the DSL file and converts it into an Ansible playbook format."""
    with open(dsl_file, 'r') as file:
        dsl_data = yaml.safe_load(file)
    
    ansible_playbook = []
    tasks = []
    
    # Install Section
    if 'install' in dsl_data:
        for item in dsl_data['install']:
            for key, value in item.items():
                tasks.append({
                    'name': f'Install {key}',
                    'shell': value,
                    'args': {'executable': '/bin/bash'}
                })
    
    # Configuration Section
    if 'configure' in dsl_data:
        for key, value in dsl_data['configure'].items():
            tasks.append({
                'name': f'Configure {key}',
                'lineinfile': {
                    'path': value['path'],
                    'line': f'export {key.upper()}={value['export']}',
                    'create': True,
                    'state': 'present'
                }
            })
    
    # Firewall Rules
    if 'firewall' in dsl_data:
        for rule in dsl_data['firewall']['allow']:
            tasks.append({
                'name': f'Allow Firewall Port {rule['port']}/{rule['proto']}',
                'community.general.ufw': {
                    'rule': 'allow',
                    'port': rule['port'],
                    'proto': rule['proto']
                }
            })
    
    # Helm Installation
    if 'helm' in dsl_data:
        tasks.append({
            'name': 'Check if Helm is installed',
            'command': dsl_data['helm']['check'],
            'register': 'helm_check',
            'ignore_errors': True,
            'changed_when': False
        })
        tasks.append({
            'name': 'Install Helm',
            'command': dsl_data['helm']['install'],
            'when': 'helm_check.rc != 0'
        })
    
    # Cilium Installation
    if 'cilium' in dsl_data:
        tasks.append({
            'name': 'Add Cilium Helm Repository',
            'kubernetes.core.helm_repository': {
                'name': 'cilium',
                'repo_url': dsl_data['cilium']['helm']['repo']
            }
        })
        tasks.append({
            'name': 'Install Cilium',
            'kubernetes.core.helm': {
                'name': 'cilium',
                'chart_ref': 'cilium/cilium',
                'release_namespace': 'kube-system',
                'create_namespace': True,
                'values': dsl_data['cilium']['helm']['install']['values']
            },
            'environment': {'KUBECONFIG': '/etc/rancher/k3s/k3s.yaml'}
        })
        tasks.append({
            'name': 'Wait for Cilium Pods',
            'command': dsl_data['cilium']['wait'],
            'register': 'cilium_pod_status',
            'until': 'cilium_pod_status.rc == 0',
            'retries': 10,
            'delay': 10
        })
        tasks.append({
            'name': 'Run Cilium Connectivity Test',
            'command': dsl_data['cilium']['test'],
            'register': 'connectivity_test',
            'failed_when': 'connectivity_test.rc != 0'
        })
    
    # Monitoring Tools
    if 'monitoring' in dsl_data:
        for tool, url in dsl_data['monitoring'].items():
            tasks.append({
                'name': f'Install {tool}',
                'kubernetes.core.k8s': {
                    'state': 'present',
                    'src': url
                }
            })
    
    # Final Verification
    if 'verify' in dsl_data:
        for key, command in dsl_data['verify'].items():
            tasks.append({
                'name': f'Verify {key}',
                'command': command,
                'register': f'{key}_status'
            })
            tasks.append({
                'name': f'Display {key} Status',
                'debug': {'msg': f'{{{{ {key}_status.stdout }}}}'}}
            )
    
    ansible_playbook.append({
        'name': 'Generated Ansible Playbook from DSL',
        'hosts': 'localhost',
        'become': True,
        'tasks': tasks
    })
    
    return ansible_playbook


def main():
    if len(sys.argv) != 2:
        print("Usage: python dsl_to_ansible.py <dsl_file>")
        sys.exit(1)
    
    dsl_file = sys.argv[1]
    playbook = parse_dsl(dsl_file)
    print(yaml.dump(playbook, default_flow_style=False))


if __name__ == "__main__":
    main()
