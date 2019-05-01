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

import charms.apt
import os
import shutil


@when_any('config.changed', 'apt.installed.newrelic-infra')
def configure_agent():
    status_set('waiting', "Initializing New Relic Infrastructure Agent")
    set_flag('layer-newrelic-infra.license_key.update')

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


@when('nri_elasticsearch.included')
@when_not('apt.installed.nri-elasticsearch')
def install_nri_elasticsearch():
    status_set('waiting', "Installing nri-elasticsearch")
    charms.apt.queue_install(['nri-elasticsearch'])


@when('apt.installed.nri-elasticsearch')
def configure_nri_elasticsearch():
    status_set('waiting', "Configuring nri-elasticsearch")
    os.chdir('/etc/newrelic-infra/integrations.d')
    shutil.copyfile('elasticsearch-config.yml.sample', 'elasticsearch-config.yml')


@when('nri_redis.included')
@when_not('apt.installed.nri-redis')
def install_nri_redis():
    status_set('waiting', "Installing nri-redis")
    charms.apt.queue_install(['nri-redis'])


@when('apt.installed.nri-redis')
def configure_nri_redis():
    status_set('waiting', "Configuring nri-redis")
    os.chdir('/etc/newrelic-infra/integrations.d')
    shutil.copyfile('redis-config.yml.sample', 'redis-config.yml')
