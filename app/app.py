from utils import app, swaggerui_blueprint, SWAGGER_URL
from utils.seed import seed_database
from routes import app_routes
from api.invoices import invoices_bp
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'seeder':
        seed_database()
    app.register_blueprint(app_routes)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.run()
