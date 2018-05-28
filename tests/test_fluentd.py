import unittest
from unittest import mock
import os
import json
from freezegun import freeze_time

from fluentdmetrics.fluentd import get_fluentd_plugin_info

from responses import RequestsMock
from tests import get_fixture

class FluentdTest(unittest.TestCase):

    def setUp(self):
        self.plugin_info_fixture = get_fixture("./fixtures/fluentd-plugins-all-zeroed.json")
        self.plugin_info_with_retries_fixture = get_fixture("./fixtures/fluentd-plugins-flush-failed-retrying.json")
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

            self.assertEqual(plugin_info['10.0.0.4']["retry_count"], 0)
            self.assertEqual(plugin_info['10.0.0.4']["buffer_total_queued_size"], 0)
            self.assertEqual(plugin_info['10.0.0.4']["output_plugin"], True)
            self.assertEqual(plugin_info['10.0.0.4']["retry"], {})
            self.assertEqual(plugin_info['10.0.0.4']["buffer_queue_length"], 0)

    def test_get_infos_one_plugin_multiple_servers(self):
        with RequestsMock() as rsps, \
                mock.patch.dict(os.environ,
                                HOLLOWMAN_FLUENTD_ADDRESS_0="http://10.0.0.4:24224",
                                HOLLOWMAN_FLUENTD_ADDRESS_1="http://10.0.0.5:24224"):
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(self.plugin_info_fixture), status=200)
            rsps.add(method="GET", url="http://10.0.0.5:24224/api/plugins.json", body=json.dumps(self.plugin_info_fixture), status=200)
            plugin_info = get_fluentd_plugin_info("app-logs-out-rabbitmq")
            self.assertTrue("10.0.0.4" in plugin_info)
            self.assertTrue("10.0.0.5" in plugin_info)

            self.assertEqual("app-logs-out-rabbitmq", plugin_info['10.0.0.4']['plugin_id'])
            self.assertEqual(plugin_info['10.0.0.4']["retry_count"], 0)
            self.assertEqual(plugin_info['10.0.0.4']["buffer_total_queued_size"], 0)
            self.assertEqual(plugin_info['10.0.0.4']["output_plugin"], True)
            self.assertEqual(plugin_info['10.0.0.4']["retry"], {})
            self.assertEqual(plugin_info['10.0.0.4']["buffer_queue_length"], 0)

            self.assertEqual("app-logs-out-rabbitmq", plugin_info['10.0.0.5']['plugin_id'])
            self.assertEqual(plugin_info['10.0.0.5']["retry_count"], 0)
            self.assertEqual(plugin_info['10.0.0.5']["buffer_total_queued_size"], 0)
            self.assertEqual(plugin_info['10.0.0.5']["output_plugin"], True)
            self.assertEqual(plugin_info['10.0.0.5']["retry"], {})
            self.assertEqual(plugin_info['10.0.0.5']["buffer_queue_length"], 0)

    def test_get_infos_one_plugin_with_retry_count_more_than_one_hour(self):
        """
        Testa o cálculo da da hora do retry com mais de uma hora de diferença
        """
        with RequestsMock() as rsps, \
                freeze_time("2018-05-24 13:50:00 +0000"):
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(self.plugin_info_with_retries_fixture), status=200)
            plugin_info = get_fluentd_plugin_info("app-logs-out-rabbitmq")
            self.assertTrue("10.0.0.4" in plugin_info)
            self.assertEqual("app-logs-out-rabbitmq", plugin_info['10.0.0.4']['plugin_id'])

            self.assertEqual(plugin_info['10.0.0.4']["retry_count"], 5)
            self.assertEqual(plugin_info['10.0.0.4']["buffer_total_queued_size"], 192640)
            self.assertEqual(plugin_info['10.0.0.4']["buffer_queue_length"], 0)
            self.assertEqual(plugin_info['10.0.0.4']["retry_next_min"], 4 * 60) # 4 horas até a próxima tentativa

    def test_get_infos_one_plugin_with_retry_count(self):
        """
        Testa o cálculo da da hora do retry com menos de uma hora de diferença
        """
        with RequestsMock() as rsps, \
                freeze_time("2018-05-24 17:45:00 +0000"):
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(self.plugin_info_with_retries_fixture), status=200)
            plugin_info = get_fluentd_plugin_info("app-logs-out-rabbitmq")
            self.assertTrue("10.0.0.4" in plugin_info)
            self.assertEqual("app-logs-out-rabbitmq", plugin_info['10.0.0.4']['plugin_id'])

            self.assertEqual(plugin_info['10.0.0.4']["retry_count"], 5)
            self.assertEqual(plugin_info['10.0.0.4']["buffer_total_queued_size"], 192640)
            self.assertEqual(plugin_info['10.0.0.4']["buffer_queue_length"], 0)
            self.assertEqual(plugin_info['10.0.0.4']["retry_start_min"], -1)
            self.assertEqual(plugin_info['10.0.0.4']["retry_next_min"], 5)

    def test_get_info_for_non_existent_plugin(self):
        with RequestsMock() as rsps:
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(self.plugin_info_fixture), status=200)
            plugin_info = get_fluentd_plugin_info("app-logs-out-rabbitmq-do-not-exist")
            self.assertTrue("10.0.0.4" in plugin_info)
            self.assertEqual({}, plugin_info['10.0.0.4'])
