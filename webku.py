from flask import Flask, request, send_file, render_template_string
import os, subprocess, uuid, tempfile
from PIL import Image

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HARIS DOWNLOADER</title>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#0a0000;color:#fff;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
.box{background:#1a0000;border:2px solid #ff1a1a44;padding:25px;border-radius:20px;width:100%;max-width:380px;text-align:center}
.logo{width:100px;height:100px;margin:0 auto 15px;border-radius:20px;background:#111;border:2px solid #ff1a1a;display:flex;justify-content:center;align-items:center;font-size:50px}
h2{color:#ff1a1a;margin-bottom:15px}
input{width:100%;padding:12px;border-radius:10px;background:#000;border:1px solid #444;color:#fff;margin-bottom:10px;text-align:center}
.btn{width:100%;padding:12px;border:none;border-radius:10px;font-weight:bold;margin-bottom:8px;cursor:pointer}
.red{background:#ff0000;color:#fff}.dark{background:#111;border:1px solid #ff1a1a33;color:#ff1a1a}.white{background:#fff;color:#000}
.row{display:flex;gap:8px}.row.btn{flex:1}
.msg{margin-top:10px;background:#00ff8822;padding:8px;border-radius:8px;font-size:12px;word-break:break-all}
</style></head><body>
<div class="box"><div class="logo">🔥</div><h2>HARIS PRIBADI DOWNLOADER</h2>
<form method="POST" enctype="multipart/form-data">
<input type="text" name="url" placeholder="Paste link TT/YT/IG/FB">
<input type="file" name="file">
<button formaction="/download_video" class="btn red">DOWNLOAD VIDEO</button>
<div class="row">
<button formaction="/stiker_foto" class="btn dark">STIKER FOTO</button>
<button formaction="/hd_foto" class="btn dark">HD FOTO</button>
</div>
</form>
{% if msg %}<div class="msg">{{msg}}</div>{% endif %}
<p style="margin-top:15px;font-size:11px;color:#666">webkudownloader.vercel.app</p>
</div></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, msg=None)

@app.route('/download_video', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return render_template_string(HTML, msg="Paste link dulu bos!")
    try:
        tmpdir = tempfile.mkdtemp()
        out = os.path.join(tmpdir, "%(title)s.%(ext)s")
        cmd = f'yt-dlp -o "{out}" "{url}"'
        subprocess.run(cmd, shell=True, check=True, timeout=60)
        files = [os.path.join(tmpdir,f) for f in os.listdir(tmpdir)]
        if not files:
            return render_template_string(HTML, msg="Gagal download, cek link!")
        return send_file(files[0], as_attachment=True)
    except Exception as e:
        return render_template_string(HTML, msg=f"Error: {str(e)[:200]}")

@app.route('/stiker_foto', methods=['POST'])
def stiker_foto():
    f = request.files.get('file')
    if not f or f.filename == '':
        return render_template_string(HTML, msg="Upload foto dulu!")
    try:
        tmpdir = tempfile.mkdtemp()
        pin = os.path.join(tmpdir, "in.jpg")
        pout = os.path.join(tmpdir, "out.webp")
        f.save(pin)
        im = Image.open(pin).convert("RGBA")
        im.thumbnail((512,512))
        new = Image.new("RGBA",(512,512),(0,0,0,0))
        new.paste(im, ((512-im.width)//2,(512-im.height)//2))
        new.save(pout, "WEBP")
        return send_file(pout, as_attachment=True, download_name="stiker.webp")
    except Exception as e:
        return render_template_string(HTML, msg=f"Error: {e}")

@app.route('/hd_foto', methods=['POST'])
def hd_foto():
    f = request.files.get('file')
    if not f or f.filename == '':
        return render_template_string(HTML, msg="Upload foto dulu!")
    try:
        tmpdir = tempfile.mkdtemp()
        pin = os.path.join(tmpdir, "in.jpg")
        pout = os.path.join(tmpdir, "hd.jpg")
        f.save(pin)
        im = Image.open(pin)
        w,h = im.size
        im.resize((w*2,h*2), Image.LANCZOS).save(pout)
        return send_file(pout, as_attachment=True, download_name="HD.jpg")
    except Exception as e:
        return render_template_string(HTML, msg=f"Error: {e}")

if __name__ == '__main__':
    app.run()
