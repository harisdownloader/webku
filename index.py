from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '<h1 style="background:#000;color:#f00;text-align:center;padding:50px">🔥 HARIS DOWNLOADER ONLINE BOS! 🔥<br><br>webkudownloader.vercel.app</h1>'

@app.route('/<path:p>')
def all(p): return home()
