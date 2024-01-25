from utils import app
from utils.seed import seed_database
from routes import app_routes
from api.invoices import invoices_bp
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'seeder':
        seed_database()
    app.register_blueprint(app_routes)
    app.register_blueprint(invoices_bp)
    app.run()
