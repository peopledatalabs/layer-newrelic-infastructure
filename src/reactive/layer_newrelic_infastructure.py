from charms.reactive import (
    when,
    when_not,
    set_flag,
)

from charmhelpers.core.hookenv import (
    config,
    status_set,
)


@when_not('layer-newrelic-infrastructure.installed')
def install_layer_newrelic_infrastructure():
    set_flag('layer-newrelic-infrastructure.installed')


@when('config.changed', 'layer-newrelic-infrastructure.installed')
def set_license_key():
    status_set('waiting', "Initializing New Relic Infrastructure Agent")

    if config('license_key'):
        newrelic_infra_yml = open("/etc/newrelic-infra.yml", "w")
        newrelic_infra_yml.write("license_key: " + config('license_key'))

        status_set('active', "New Relic Infrastructure Agent Ready")
        set_flag('license-key.set')
    else:
        status_set('blocked', "Missing New Relic License Key")
