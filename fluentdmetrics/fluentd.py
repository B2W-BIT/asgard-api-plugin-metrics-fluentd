from urllib.parse import urlparse
from datetime import datetime
from collections import defaultdict

import pytz
from dateutil.parser import parse

from asgard.sdk.options import get_option
import requests

def get_fluentd_server_addresses():
    return get_option("FLUENTD", "ADDRESS")

def get_fluentd_plugin_info(plugin_id):
    result = {}
    now  =  datetime.now(tz=pytz.utc)
    for addr in get_fluentd_server_addresses():
        server_ip = urlparse(addr).hostname
        result[server_ip] = {}
        response = requests.get(f"{addr}/api/plugins.json", timeout=2)
        response_data = response.json()
        plugin_data = [info for info in response_data['plugins'] if info['plugin_id'] == plugin_id]
        if plugin_data:
            if plugin_data[0]['retry']:
                plugin_data[0]['retry_start_min'] = (parse(plugin_data[0]['retry']['start']) - now).total_seconds() / 60
                plugin_data[0]['retry_next_min'] = (parse(plugin_data[0]['retry']['next_time']) - now).total_seconds() / 60
            else:
                plugin_data[0]['retry_start_min'] = 0
                plugin_data[0]['retry_next_min'] = 0

            result[server_ip] = plugin_data[0]
    return result

def get_fluentd_summary_plugin_info(plugin_id):
    """
      "retry_count": each(<IP>).sum(retry_count),
      "buffer_queue_length": each(<IP>).sum(buffer_queue_length),
      "buffer_total_queued_size": each(<IP>).sum(buffer_total_queued_size),
    """
    result = defaultdict(int)
    plugin_info = get_fluentd_plugin_info(plugin_id)
    for server_ip, plugin_data in plugin_info.items():
        result['retry_count'] += plugin_data['retry_count']
        result['buffer_queue_length'] += plugin_data['buffer_queue_length']
        result['buffer_total_queued_size'] += plugin_data['buffer_total_queued_size']
    return result
