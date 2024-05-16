import logging
import os

from flask import Flask
from redis import Redis
from flask_caching import Cache

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

CACHE_CARD_PRICE_KEY = "card_price"
BASE_REDIS_EXPIRATION = 60 * 60 * 24

config = {
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_DB,
    "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app=app)
cache.init_app(app)
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Configure Flask logging
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Importing the other views
from src.views import *  # noqa


def make_key(*args, **kwargs):
    user_data = request.get_json()  # noqa: F405
    return ",".join([f"{key}={value}" for key, value in user_data.items()])


@app.route("/")
def index():
    app.logger.info("This is an INFO message")
    app.logger.debug("This is a DEBUG message")
    app.logger.warning("This is a WARNING message")
    app.logger.error("This is an ERROR message")
    app.logger.critical("This is a CRITICAL message")
    return "Hello, World!"


if __name__ == "__main__":
    app.run(reloader=True, debug=True)
    # obj = {
    #     "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Kouzuki+Oden+%28OP01-031-PAR%29&ed=OP-01&num=OP01-031-PAR",  # noqa
    #     "card_name": "Kouzuki Oden (OP01-031-PAR)"
    # }
    # price = get_price_workflow(obj["url"])
