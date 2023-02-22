from flask import Blueprint

from routes.api.v1.ekart import ekart

urlpatterns = [
    ("/ekart", ekart),
]

v1 = Blueprint("v1", __name__)

for prefix, blueprint in urlpatterns:
    v1.register_blueprint(blueprint, url_prefix=prefix)
