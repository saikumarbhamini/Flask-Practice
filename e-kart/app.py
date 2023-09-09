from flask import Flask

from routes import urlpatterns
from utilities.database import db
from utilities.serializer import ma
from utilities.migrations import migrate
import settings


def create_application():
    application = Flask(__name__)
    application.config.update(
        DEBUG=settings.DEBUG,
        SERVER_NAME=f"{settings.HOST}:{settings.PORT}",
        SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=settings.SQLALCHEMY_TRACK_MODIFICATIONS,
    )

    db.init_app(application)
    ma.init_app(application)

    migrate.init_app(application, db)

    # with application.app_context():
    #     db.create_all()

    for prefix, blueprint in urlpatterns:
        application.register_blueprint(blueprint, url_prefix=prefix)

    return application


application = create_application()

if __name__ == "__main__":
    application.run()
