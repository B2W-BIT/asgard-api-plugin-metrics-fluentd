import json
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


from flask import Response
import pytz

from fluentdmetrics.blueprint import fluentd_metrics_blueprint
from fluentdmetrics import fluentd

@fluentd_metrics_blueprint.route('/plugins/<string:plugin_id>')
def one_plugin(plugin_id):
    plugin_info = fluentd.get_fluentd_plugin_info(plugin_id)
    plugin_exist = any([plugin_data for plugin_id, plugin_data in plugin_info.items()])
    if plugin_exist:
        final_result = {}
        for server_ip, plugin_data in plugin_info.items():
            now = datetime.now(pytz.utc)
            final_result.update({
                 f"retry_start_min_{server_ip}": plugin_data['retry_start_min'],
                 f"retry_next_min_{server_ip}": plugin_data['retry_next_min'],
                 f"buffer_queue_length_{server_ip}" : plugin_data['buffer_queue_length'],
                 f"retry_count_{server_ip}" : plugin_data['retry_count'],
                 f"buffer_total_queued_size_{server_ip}" : plugin_data['buffer_total_queued_size'],
            })
        return Response(
            json.dumps(final_result),
            mimetype='application/json'
        )
    return Response(status=404, mimetype='application/json')

@fluentd_metrics_blueprint.route('/retry_count/<string:plugin_id>')
def retry_count(plugin_id):
    return Response(
        json.dumps(fluentd.get_fluentd_summary_plugin_info(plugin_id)),
        mimetype='application/json'
    )
