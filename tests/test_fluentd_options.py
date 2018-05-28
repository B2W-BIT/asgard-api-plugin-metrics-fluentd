import unittest
from unittest.mock import patch
import os

from fluentdmetrics.fluentd import get_fluentd_server_addresses

class FluentdOptionsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_address_from_env_vars(self):
        address_0 = "http://10.0.0.4:24224"
        expected_addresses = [address_0]
        with patch.dict(os.environ, HOLLOWMAN_FLUENTD_ADDRESS_0=address_0):
            addresses = get_fluentd_server_addresses()
            self.assertEqual(expected_addresses, addresses)

    def test_get_address_more_than_one_value(self):
        address_0 = "http://10.0.0.4:24224"
        address_1 = "http://10.0.0.5:24224"
        address_2 = "http://10.0.0.6:24224"
        expected_addresses = [address_0, address_1, address_2]
        with patch.dict(os.environ,
                        HOLLOWMAN_FLUENTD_ADDRESS_0=address_0,
                        HOLLOWMAN_FLUENTD_ADDRESS_1=address_1,
                        HOLLOWMAN_FLUENTD_ADDRESS_2=address_2):
            addresses = get_fluentd_server_addresses()
            self.assertEqual(expected_addresses, addresses)
