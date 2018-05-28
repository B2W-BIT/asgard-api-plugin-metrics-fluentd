from asgard.sdk.options import get_option

def get_fluentd_server_addresses():
    return get_option("FLUENTD", "ADDRESS")
