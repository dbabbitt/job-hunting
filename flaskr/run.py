from app.consumer import start_consumer
from app.dash_app import run_dash
from app.server import run_flask
from threading import Thread

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    dash_thread = Thread(target=run_dash)
    consumer_thread = Thread(target=start_consumer)
    
    flask_thread.start()
    dash_thread.start()
    consumer_thread.start()
    
    flask_thread.join()
    dash_thread.join()
    consumer_thread.join()