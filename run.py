#This is where I will run the application to keep it easier to understand. The application must be ran from python run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)