# ansible-ct-filter
Container Linux Config Transpiler filter for Ansible. 
Filters a [Container Linux Configuration YAML](https://coreos.com/os/docs/latest/configuration.html) into an [Ignition Configuration](https://coreos.com/ignition/docs/latest/configuration-v2_0.html).

## Dependencies
* `ct` binary: https://github.com/coreos/container-linux-config-transpiler/releases
  * Expected in `./bin`

### Typical working directory
```
./filter_plugins/cy.py
./bin/ct
```

## Usage
```yaml
# Platform argument to ct() required.
# Note the usage of the string filter. This prevents
#   the resulting json object from being marshalled
#   into a dictionary.
user_data: "{{ container_linux_config_data | ct('ec2') | string }}"
```

### In a playbook
```yaml
---
- hosts: localhost
  vars:
    cl_config:
      etcd:
        version: 3.0.15
        name: '{HOSTNAME}'
        listen_client_urls: >
          http://{PRIVATE_IPV4}:2379,
          http://localhost:2379
        discovery_srv: 'example.com'
        proxy: 'on'
      locksmith:
        reboot_strategy: 'etcd-lock'
      update:
        group: 'stable'
      flannel:
        version: 0.7.0
      systemd:
        units:
          - name: flanneld.service
            enable: true
            dropins:
              - name: 50-network-config.conf
                contents: |
                  [Service]
                  ExecStartPre=/usr/bin/etcdctl set /coreos.com/network/config \
                    "{\"Network\":\"10.10.41.0/20\", \
                      \"SubnetLen\": 28, \
                      \"SubnetMin\": \"10.10.41.0\", \
                      \"SubnetMax\": \"10.10.47.240\" \
                    }"
  tasks:
    - debug:
        msg: "{{cl_config|ct('ec2')}}"
```
