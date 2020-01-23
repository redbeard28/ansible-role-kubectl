import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture
def get_ansiblevars(host):
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files = "file=../../vars/main.yml name=role_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])
    print(ansible_vars)
    return ansible_vars


# Verify if folder exist
def test_terraform_dir_path(host, get_ansiblevars):
    kubectl_bin_path = "%s-%s" % (get_ansiblevars['kubectl_folder'], get_ansiblevars['kubectl_version'])
    bin_path = host.file(kubectl_bin_path)
    assert bin_path.exists
    assert bin_path.user == 'root'
    assert bin_path.group == 'root'


# Verify if terraform_dir exist
def test_terraform_dir_file(host, get_ansiblevars):
    kubectl_bin_file = "%s-%s/kubectl" % (get_ansiblevars['kubectl_folder'], get_ansiblevars['kubectl_version'])
    file = host.file(kubectl_bin_file)
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.mode == 755
