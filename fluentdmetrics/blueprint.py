from flask import Blueprint

fluentd_metrics_blueprint = Blueprint(__name__, __name__)

# Para que as rotas sejam registradas
from fluentdmetrics.api import routes
