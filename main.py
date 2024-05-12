from website._init_ import create_app
from flask_migrate import Migrate
# If you want to update the tables, delete every tables and run this command on terminal: 
# set FLASK_APP=main.py
#python -m flask db init
#python -m flask db migrate
#python -m flask db upgrade
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
