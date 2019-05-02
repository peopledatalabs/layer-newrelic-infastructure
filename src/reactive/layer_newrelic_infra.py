from charms.reactive import (
    when,
    when_any,
    when_not,
    set_flag,
    clear_flag,
)

from charmhelpers.core.hookenv import (
    config,
    status_set,
)

from charmhelpers.core.host import (
    service_restart,
)

import charms.apt
import shutil


@when_any('config.changed')
def configure_agent():
    clear_flag('newrelic-infra.ready')
    status_set('waiting', "Configuring New Relic Infrastructure Agent")

    set_flag('newrelic-infra.license_key.update')

    if config('include_nri_elasticsearch'):
        set_flag('nri_elasticsearch.included')
    else:
        clear_flag('nri_elasticsearch.included')

    if config('include_nri_redis'):
        set_flag('nri_redis.included')
    else:
        clear_flag('nri_redis.included')


@when('newrelic-infra.license_key.update')
def set_license_key():
    if not config('license_key'):
        status_set('blocked', "Missing New Relic License Key")
    else:
        newrelic_infra_yml = open("/etc/newrelic-infra.yml", "w")
        newrelic_infra_yml.write("license_key: " + config('license_key'))

        clear_flag('newrelic-infra.license_key.update')
        set_flag('newrelic-infra.ready')


@when('nri_elasticsearch.included')
@when_not('apt.installed.nri-elasticsearch')
def install_nri_elasticsearch():
    status_set('waiting', "Installing nri-elasticsearch")
    charms.apt.queue_install(['nri-elasticsearch'])


@when('apt.installed.nri-elasticsearch')
@when_not('nri-elasticsearch.configured')
def configure_nri_elasticsearch():
    status_set('waiting', "Configuring nri-elasticsearch")
    shutil.copyfile('/etc/newrelic-infra/integrations.d/elasticsearch-config.yml.sample',
                    '/etc/newrelic-infra/integrations.d/elasticsearch-config.yml')
    set_flag('nri-elasticsearch.configured')
    set_flag('newrelic-infra.ready')


@when('nri_redis.included')
@when_not('apt.installed.nri-redis')
def install_nri_redis():
    status_set('waiting', "Installing nri-redis")
    charms.apt.queue_install(['nri-redis'])


@when('apt.installed.nri-redis')
@when_not('nri-redis.configured')
def configure_nri_redis():
    status_set('waiting', "Configuring nri-redis")
    shutil.copyfile('/etc/newrelic-infra/integrations.d/redis-config.yml.sample',
                    '/etc/newrelic-infra/integrations.d/redis-config.yml')
    set_flag('nri-redis.configured')
    set_flag('newrelic-infra.ready')


@when('newrelic-infra.ready')
def newrelic_infra_ready():
    service_restart('newrelic-infra')
    status_set('active', "New Relic Infrastructure Agent Ready")
