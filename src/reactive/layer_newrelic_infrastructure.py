from charms.reactive import (
    when,
    when_any,
    when_not,
    set_flag,
)

from charmhelpers.core.hookenv import (
    config,
    status_set,
)


@when_not('layer-newrelic-infrastructure.installed')
def install_layer_newrelic_infrastructure():
    status_set('waiting', "Initializing New Relic Infrastructure Agent")
    set_flag('layer-newrelic-infrastructure.installed')


@when_any('config.changed', 'layer-newrelic-infrastructure.installed')
def set_license_key():
    if not config('license_key'):
        status_set('blocked', "Missing New Relic License Key")

    newrelic_infra_yml = open("/etc/newrelic-infra.yml", "w")
    newrelic_infra_yml.write("license_key: " + config('license_key'))
    status_set('active', "New Relic Infrastructure Agent Ready")
