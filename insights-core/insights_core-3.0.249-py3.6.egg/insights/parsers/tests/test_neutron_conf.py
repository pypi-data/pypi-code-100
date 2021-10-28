from insights.parsers.neutron_conf import NeutronConf
from insights.tests import context_wrap

NEUTRON_CONF = """
[DEFAULT]
# debug = False
debug = False
# verbose = True
verbose = False
core_plugin =neutron.plugins.openvswitch.ovs_neutron_plugin.OVSNeutronPluginV2

[quotas]
default_quota = -1
quota_network = 10
[agent]
report_interval = 60

[keystone_authtoken]
auth_host = ost-controller-lb-del.om-l.dsn.inet
auth_port = 35357
[database]
connection = mysql://neutron:dSNneutron01@ost-mysql.om-l.dsn.inet/neutron?ssl_ca=/etc/pki/CA/certs/ca.crt
[service_providers]
service_provider = LOADBALANCER:Haproxy:neutron.services.loadbalancer.drivers.haproxy.plugin_driver.HaproxyOnHostPluginDriver:default
"""


def test_neutron_conf():
    nconf = NeutronConf(context_wrap(NEUTRON_CONF))
    assert nconf is not None
    assert list(nconf.sections()) == ['quotas', 'agent', 'keystone_authtoken', 'database', 'service_providers']
    assert nconf.defaults() == {
        'debug': 'False',
        'verbose': 'False',
        'core_plugin': 'neutron.plugins.openvswitch.ovs_neutron_plugin.OVSNeutronPluginV2'}
    assert nconf.get('quotas', 'quota_network') == '10'
    assert nconf.has_option('database', 'connection')
    assert not nconf.has_option('yabba', 'dabba_do')
    assert nconf.get('DEFAULT', 'debug') == 'False'
