import unittest

from fluentdmetrics.plugin import asgard_api_plugin_init
from fluentdmetrics.blueprint import fluentd_metrics_blueprint

class PluginEntrypointTest(unittest.TestCase):

    def test_return_correct_blueprint(self):
        self.assertTrue(asgard_api_plugin_init()['blueprint'] is fluentd_metrics_blueprint)
