from charms.reactive import when, when_not, set_flag
from charmhelpers.core.hookenv import status_set
import charms.apt

from charmhelpers.core.hookenv import (
    config,
)


@when_not('layer-newrelic-infastructure.installed')
def install_layer_newrelic_infastructure():
    newrelic_infra_yml = open("/etc/newrelic-infra.yml", "w")
    newrelic_infra_yml.write("license_key: " + config('license_key'))
    status_set('active', "Installed")
    set_flag('layer-newrelic-infastructure.installed')

# @when('layer-newrelic-infastucture.installed')
# @when_not('license-key.set')
# def set_license_key():
#     set_flag('license-key.set')
