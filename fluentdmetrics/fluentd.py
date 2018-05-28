from urllib.parse import urlparse

from asgard.sdk.options import get_option
import requests

def get_fluentd_server_addresses():
    return get_option("FLUENTD", "ADDRESS")

def get_fluentd_plugin_info(plugin_id):
    result = {}
    for addr in get_fluentd_server_addresses():
        server_ip = urlparse(addr).hostname
        result[server_ip] = {}
        response = requests.get(f"{addr}/api/plugins.json", timeout=2)
        response_data = response.json()
        plugin_data = [info for info in response_data['plugins'] if info['plugin_id'] == plugin_id]
        if plugin_data:
            result[server_ip] = plugin_data[0]
    return result
