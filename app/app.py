import os
import time
import base64
from io import BytesIO

import redis
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    password=os.getenv("REDIS_PASSWORD"),
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "titanic.csv")


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route("/")
def home():
    count = get_hit_count()
    return render_template("home.html", name="BIPM", count=count)


@app.route("/titanic")
def titanic():
    df = pd.read_csv(DATA_PATH)
    survived_by_sex = (
        df.groupby("Sex")["Survived"].mean().mul(100).round(1)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    survived_by_sex.plot(kind="bar", ax=ax, color=["#4c72b0", "#dd8452"])
    ax.set_ylabel("Survival rate (%)")
    ax.set_xlabel("Gender")
    ax.set_title("Titanic survival rate by gender")
    plt.xticks(rotation=0)
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    chart = base64.b64encode(buf.getvalue()).decode("utf-8")

    table = df.head(10).to_html(classes="titanic-table", index=False)
    return render_template("titanic.html", chart=chart, table=table)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
