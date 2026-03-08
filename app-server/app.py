from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db():
    conn = psycopg2.connect(
        host="192.168.56.12",
        database="homelabdb",
        user="labuser",
        password="labpassword"
    )
    return conn

@app.route("/")
def home():
    return "Homelab App Running"

@app.route("/db")
def test_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    conn.close()
    return f"Database connected: {db_version}"

app.run(host="0.0.0.0", port=5000)
