import unittest
from unittest import mock
import os
import json

from fluentdmetrics.fluentd import get_fluentd_plugin_info

from responses import RequestsMock
from tests import get_fixture

class FluentdTest(unittest.TestCase):

    def setUp(self):
        self.plugin_info_fixture = get_fixture("./fixtures/fluentd-plugins-all-zeroed.json")
        self.env_patcher = mock.patch.dict(os.environ, HOLLOWMAN_FLUENTD_ADDRESS_0="http://10.0.0.4:24224")
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    def test_get_infos_for_one_plugin(self):
        """
        Retornamos os dados em um dict, com a chave sendo o IP do servidor e o valor sendo
        o JSON original desse plugin, vindo do fluentd
        """
        with RequestsMock() as rsps:
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(self.plugin_info_fixture), status=200)
            plugin_info = get_fluentd_plugin_info("app-logs-out-rabbitmq")
            self.assertTrue("10.0.0.4" in plugin_info)
            self.assertEqual("app-logs-out-rabbitmq", plugin_info['10.0.0.4']['plugin_id'])

    def test_get_info_for_non_existent_plugin(self):
        with RequestsMock() as rsps:
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(self.plugin_info_fixture), status=200)
            plugin_info = get_fluentd_plugin_info("app-logs-out-rabbitmq-do-not-exist")
            self.assertTrue("10.0.0.4" in plugin_info)
            self.assertEqual({}, plugin_info['10.0.0.4'])
