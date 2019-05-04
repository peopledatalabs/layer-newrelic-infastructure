from charms.reactive import (
    when,
    when_any,
    set_flag,
    clear_flag,
    hook,
)

from charmhelpers.core.hookenv import (
    config,
    status_set,
)

from charmhelpers.core.host import (
    service_restart,
)

import charms.apt
import os


@when_any('config.changed')
def configure_agent():
    status_set('waiting', "Configuring New Relic Infrastructure Agent")
    clear_flag('newrelic-infra.ready')
    set_flag('newrelic-infra.license_key.update')


@when('newrelic-infra.license_key.update')
def set_license_key():
    if not config('license_key'):
        if os.path.isfile("/etc/newrelic-infra.yml"):
            os.remove("/etc/newrelic-infra.yml")

        status_set('blocked', "Missing New Relic License Key")
    else:
        newrelic_infra_yml = open("/etc/newrelic-infra.yml", "w")
        newrelic_infra_yml.write("license_key: " + config('license_key'))

        clear_flag('newrelic-infra.license_key.update')
        set_flag('newrelic-infra.ready')


@when('newrelic-infra.ready')
def newrelic_infra_ready():
    service_restart('newrelic-infra')
    status_set('active', "New Relic Infrastructure Agent Ready")


@hook('stop')
def remove_newrelic_infra():
    status_set('maintenance', "Removing New Relic Infrastructure Agent")

    if os.path.isfile("/etc/newrelic-infra.yml"):
        os.remove("/etc/newrelic-infra.yml")

    clear_flag('newrelic-infra.ready')
    charms.apt.purge(['newrelic-infra'])
