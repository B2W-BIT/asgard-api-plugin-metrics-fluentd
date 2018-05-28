from flask import Flask
import unittest
from unittest import mock

from responses import RequestsMock
import json
from freezegun import freeze_time

from tests import get_fixture
from fluentdmetrics.blueprint import fluentd_metrics_blueprint

class ApiRoutesTest(unittest.TestCase):

    def setUp(self):
        self.application = Flask(__name__)
        self.application.register_blueprint(fluentd_metrics_blueprint, url_prefix="")
        self.get_fluentd_server_addresses_patcher = mock.patch('fluentdmetrics.fluentd.get_fluentd_server_addresses', return_value=["http://10.0.0.4:24224"])
        self.get_fluentd_server_addresses_mock = self.get_fluentd_server_addresses_patcher.start()

    def tearDown(self):
        self.get_fluentd_server_addresses_patcher.stop()

    def test_read_plugin_metrics_plugin_does_not_exist(self):
        """
        Devemos retornar 404
        """
        plugins_response_fixture = get_fixture("./fixtures/fluentd-plugins-all-zeroed.json")
        client = self.application.test_client()

        with RequestsMock() as rsps:
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(plugins_response_fixture), status=200)
            response = client.get("/plugins/plugin-does-not-exist")
            self.assertEqual(404, response.status_code)

    def test_read_plugin_metrics_one_server(self):
        plugins_response_fixture = get_fixture("./fixtures/fluentd-plugins-flush-failed-retrying.json")
        client = self.application.test_client()

        with RequestsMock() as rsps, \
                freeze_time("2018-05-24 17:45:00 +0000"):
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(plugins_response_fixture), status=200)
            response = client.get("/plugins/app-logs-out-rabbitmq")
            self.assertEqual(200, response.status_code)
            expected_plugin_data = {
                 "retry_start_min_10.0.0.4": -1,
                 "retry_next_min_10.0.0.4": 5,
                 "buffer_queue_length_10.0.0.4" : 0,
                 "retry_count_10.0.0.4" : 5,
                 "buffer_total_queued_size_10.0.0.4" : 192640,
            }
            response_json = json.loads(response.data)
            self.assertEqual(expected_plugin_data, response_json)

    def test_read_plugin_metrics_multiple_servers(self):
        """
        Conferimos que as métricas são entregues separadas por server IP
        """
        self.maxDiff = None
        plugins_response_fixture = get_fixture("./fixtures/fluentd-plugins-flush-failed-retrying.json")
        client = self.application.test_client()
        self.get_fluentd_server_addresses_mock.return_value = ["http://10.0.0.4:24224", "http://10.0.0.5:24224"]

        with RequestsMock() as rsps, \
                freeze_time("2018-05-24 17:45:00 +0000"):
            rsps.add(method="GET", url="http://10.0.0.4:24224/api/plugins.json", body=json.dumps(plugins_response_fixture), status=200)
            rsps.add(method="GET", url="http://10.0.0.5:24224/api/plugins.json", body=json.dumps(plugins_response_fixture), status=200)
            response = client.get("/plugins/app-logs-out-rabbitmq")
            self.assertEqual(200, response.status_code)
            expected_plugin_data = {
                 "retry_start_min_10.0.0.4": -1,
                 "retry_next_min_10.0.0.4": 5,
                 "buffer_queue_length_10.0.0.4" : 0,
                 "retry_count_10.0.0.4" : 5,
                 "buffer_total_queued_size_10.0.0.4" : 192640,

                 "retry_start_min_10.0.0.5": -1,
                 "retry_next_min_10.0.0.5": 5,
                 "buffer_queue_length_10.0.0.5" : 0,
                 "retry_count_10.0.0.5" : 5,
                 "buffer_total_queued_size_10.0.0.5" : 192640,
            }
            response_json = json.loads(response.data)
            self.assertDictEqual(expected_plugin_data, response_json)

