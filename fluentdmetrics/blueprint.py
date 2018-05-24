from flask import Blueprint, Response, request
from json import dumps

fluentd_metrics_blueprint = Blueprint(__name__, __name__)

def asgard_api_plugin_init():
    return {
        'blueprint': fluentd_metrics_blueprint
    }

@fluentd_metrics_blueprint.route('/plugins/<string:plugin_id>')
def one_plugin(plugin_id):
    return Response(
        dumps({}),
        mimetype='application/json'
    )

@fluentd_metrics_blueprint.route('/retry_count/<string:plugin_id>')
def slaves_with_attrs(plugin_id):
    return Response(
        dumps({}),
        mimetype='application/json'
    )

