from flask import Flask, request, send_file, render_template_string
import os, subprocess, uuid
from PIL import Image

app = Flask(__name__)
os.makedirs("downloads", exist_ok=True)

HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>HARIS PRIBADI DOWNLOADER</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}
body{background:#0a0000;color:white;min-height:100vh;padding:20px;display:flex;justify-content:center;align-items:center}
.box{background:linear-gradient(180deg,#1a0000,#0f0000);border:2px solid #ff1a1a44;padding:25px;border-radius:20px;width:100%;max-width:380px;text-align:center;box-shadow:0 0 30px #ff000022}
.logo-box{width:140px;height:140px;margin:0 auto 15px;border-radius:20px;background:#111;border:2px solid #ff1a1a;display:flex;justify-content:center;align-items:center;font-size:60px}
h2{color:#ff1a1a;letter-spacing:2px;font-size:18px;margin-bottom:20px}
input[type=text]{width:100%;padding:13px;border-radius:12px;text-align:center;background:#000;border:1px solid #444;color:white;outline:none;margin-bottom:12px}
input[type=text]:focus{border-color:#ff1a1a}
.filebox{background:#000;border:1px solid #333;border-radius:12px;padding:8px;margin-bottom:12px}
.filebox input{font-size:12px;color:#888;width:100%}
.btn{width:100%;padding:14px;border:none;border-radius:12px;font-weight:bold;margin-bottom:10px;cursor:pointer}
.btn-red{background:linear-gradient(90deg,#ff0000,#cc0000);color:white}
.btn-dark{background:#111;border:1px solid #ff1a1a33;color:#ff1a1a}
.btn-white{background:white;color:black}
.row{display:flex;gap:10px}.row .btn{flex:1}
.msg{margin-top:15px;background:#00ff8822;padding:10px;border-radius:10px;font-size:13px}
.footer{color:#555;font-size:11px;margin-top:25px}
</style></head>
<body>
<div class="box">
<div class="logo-box">🔥</div>
<h2>HARIS PRIBADI DOWNLOADER</h2>
<form method="POST" enctype="multipart/form-data">
<input type="text" name="url" placeholder="Paste link TT/YT/IG/FB">
<div class="filebox"><input type="file" name="file"></div>
<button formaction="/download_video" class="btn btn-red">🚀 DOWNLOAD VIDEO</button>
<div class="row">
<button formaction="/stiker_video" class="btn btn-dark">STIKER VIDEO</button>
<button formaction="/stiker_foto" class="btn btn-dark">STIKER FOTO</button>
</div>
<button formaction="/hd_foto" class="btn btn-white">✨ HD IN FOTO</button>
</form>
{% if msg %}<div class="msg">{{msg}}</div>{% endif %}
<div class="footer">© 2026 HARIS PRIBADI | RED EDITION</div>
</div>
</body></html>
"""

@app.route('/')
def home(): 
    return render_template_string(HTML, msg=None)

@app.route('/download_video', methods=['POST'])
def download_video():
    url=request.form.get('url')
    if not url: 
        return render_template_string(HTML, msg="❌ Paste link dulu bos!")
    try:
        uid=str(uuid.uuid4())[:8]
        out=f"downloads/{uid}_%(title)s.%(ext)s"
        subprocess.run(f'yt-dlp -o "{out}" "{url}"', shell=True, check=True)
        files = [os.path.join("downloads",f) for f in os.listdir("downloads")]
        latest = max(files, key=os.path.getctime)
        return send_file(latest, as_attachment=True)
    except Exception as e: 
        return render_template_string(HTML, msg=f"❌ Error: {e}")

@app.route('/stiker_video', methods=['POST'])
def stiker_video():
    f=request.files.get('file')
    if not f or f.filename=='': 
        return render_template_string(HTML, msg="❌ Upload video dulu!")
    pin=f"downloads/{uuid.uuid4()}.mp4"
    pout=f"downloads/{uuid.uuid4()}.webm"
    f.save(pin)
    subprocess.run(f'ffmpeg -y -i {pin} -t 8 -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2" -c:v libvpx-vp9 -b:v 500k -an {pout}', shell=True)
    return send_file(pout, as_attachment=True, download_name="stiker_video.webm")

@app.route('/stiker_foto', methods=['POST'])
def stiker_foto():
    f=request.files.get('file')
    if not f or f.filename=='': 
        return render_template_string(HTML, msg="❌ Upload foto dulu!")
    pin=f"downloads/{uuid.uuid4()}.jpg"
    pout=f"downloads/{uuid.uuid4()}.webp"
    f.save(pin)
    im=Image.open(pin).convert("RGBA")
    im.thumbnail((512,512))
    new=Image.new("RGBA",(512,512),(0,0,0,0))
    new.paste(im,((512-im.width)//2,(512-im.height)//2))
    new.save(pout, "WEBP")
    return send_file(pout, as_attachment=True, download_name="stiker_foto.webp")

@app.route('/hd_foto', methods=['POST'])
def hd_foto():
    f=request.files.get('file')
    if not f or f.filename=='': 
        return render_template_string(HTML, msg="❌ Upload foto dulu!")
    pin=f"downloads/{uuid.uuid4()}.jpg"
    pout=f"downloads/{uuid.uuid4()}_HD.jpg"
    f.save(pin)
    im=Image.open(pin)
    w,h=im.size
    im.resize((w*2,h*2), Image.LANCZOS).save(pout)
    return send_file(pout, as_attachment=True, download_name="HD_FOTO.jpg")

if __name__=='__main__': 
    app.run(host='0.0.0.0',port=5000,debug=True)
