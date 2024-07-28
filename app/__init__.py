from flask import Flask


def create_app():
    app = Flask(__name__)

    # Set up configuration, e.g., Kafka settings
    app.config['KAFKA_BOOTSTRAP_SERVERS'] = 'localhost:9092'
    app.config['KAFKA_TOPIC'] = 'charging_sessions'

    # Register blueprints
    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
