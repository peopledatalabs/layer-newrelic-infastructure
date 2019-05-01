from pathlib import Path

from charms.reactive import (
    when,
    when_not,
)

from charmhelpers.core.hookenv import (
    config,
    status_set,
)


infra_yaml = Path('/etc/newrelic-infra.yml')


@when_not('config.set.license_key')
def no_license_key():
    if infra_yaml.is_file():
        infra_yaml.unlink()

    status_set('blocked', "Missing New Relic License Key")


@when('config.set.license_key')
def set_license_key():
    infra_yaml.write_text("license_key: " + config('license_key'))

    status_set('active', "New Relic Infrastructure Agent Ready")
