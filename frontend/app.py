from flask import Flask
from routes import main
import asyncio
import threading
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.scraper import scrape_prices    
app = Flask(__name__)

def create_app():
    app.register_blueprint(main)
    return app
async def fetch_data():
    while True:
        await scrape_prices()
        await asyncio.sleep(60)

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_data())

def mainFunction():
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_background_loop, args=(loop,), daemon=True)
    t.start()

    app = create_app()
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    mainFunction()
