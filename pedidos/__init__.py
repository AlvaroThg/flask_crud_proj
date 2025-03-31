from flask import Flask
from flask_cors import CORS  # Importa CORS
from config import config
from pedidos.adapters.articulos_adapter import ArticulosAdapter
from pedidos.helpers.pg_command import PGCommand

app = Flask(__name__, template_folder='./presentation/templates', static_folder='./presentation/static')
app.config.from_object(config["dev"])

# Habilita CORS para toda la aplicación
CORS(app, resources={r"/*": {"origins": "http://localhost:5001"}})


db = PGCommand()

articulos_repository = ArticulosAdapter(db)

from pedidos.presentation.controllers.site_controller import *
from pedidos.presentation.controllers.articulos_controller import *
from pedidos.presentation.controllers.articulos_api_controller import *