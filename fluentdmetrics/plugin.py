
from fluentdmetrics.blueprint import fluentd_metrics_blueprint

def asgard_api_plugin_init(logger):
    return {
        'blueprint': fluentd_metrics_blueprint
    }
