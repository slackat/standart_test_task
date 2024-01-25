from utils import app
from utils.seed import seed_database
from routes import app_routes
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'seeder':
        seed_database()
        print("123")
    app.register_blueprint(app_routes)
    app.run()
