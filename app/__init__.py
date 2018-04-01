from flask import Flask 
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from instance.config import engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__,
            static_folder='./static',
            instance_relative_config=True,
            instance_path=r"C:\Users\Orbit\RPOSS\instance")
app.config.from_object('config')
app.config.from_pyfile('config.py')

bcrypt = Bcrypt(app)
Session = sessionmaker(bind=engine)
db_session = Session()
from app.views import Rmod  # for circular issues
from app.owner_panel.views import Omod  # for circular issues
from app.customer_panel.views import Cmod  # for circular issues
from app.progressive_panel.views import Smod  # for circular issues
Bootstrap(app)

app.register_blueprint(Cmod)
app.register_blueprint(Rmod, url_prefix="/RPOSS")
app.register_blueprint(Omod, url_prefix="/RPOSS/owner_panel")
app.register_blueprint(Smod, url_prefix="/RPOSS/progressive_panel")
