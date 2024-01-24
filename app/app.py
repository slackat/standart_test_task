from utils import app
from utils.seed import seed_database
from routes import app_routes

if __name__ == '__main__':
    app.register_blueprint(app_routes)
    seed_database()
    app.run()
