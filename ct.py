import subprocess
import yaml

from ansible import errors
from ansible.parsing.yaml.dumper import AnsibleDumper


def ct(item, platform, strict=False):
    ''' A filter for converting Container Linux Config
    YAML to Ignition Config '''
    transformed = yaml.dump(item,
                            Dumper=AnsibleDumper,
                            allow_unicode=True)
    cmd = ['./bin/ct', '-platform=' + platform]
    if strict:
        cmd.append('-strict')
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out, err = proc.communicate(transformed)
    if proc.returncode != 0:
        raise errors.AnsibleFilterError(err)
    return out


class FilterModule(object):
    def filters(self):
        return {
            'ct': ct
        }
