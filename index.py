from flask import Flask, request, send_file, Response
import tempfile, os
from PIL import Image

app = Flask(__name__)

def page(msg=""):
    return f"""
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HARIS DOWNLOADER</title>
<style>
body{{background:#0a0000;color:#fff;font-family:sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;padding:20px}}
.box{{background:#1a0000;border:2px solid #ff1a1a44;padding:25px;border-radius:20px;width:100%;max-width:380px;text-align:center}}
h2{{color:#ff1a1a}} input{{width:100%;padding:12px;border-radius:10px;background:#000;border:1px solid #555;color:#fff;margin:10px 0}}
.btn{{width:100%;padding:12px;border:none;border-radius:10px;font-weight:bold;margin:5px 0}}
.red{{background:#ff0000;color:#fff}} .dark{{background:#222;color:#ff5555;border:1px solid #ff000044}}
</style>
</head>
<body>
<div class="box">
<h2>🔥 HARIS DOWNLOADER 🔥</h2>
<p style="font-size:12px;color:#888">webkudownloader.vercel.app</p>
<form method="POST" enctype="multipart/form-data">
<input type="text" name="url" placeholder="Paste Link TikTok/IG/YT/FB">
<input type="file" name="file">
<button formaction="/api/index?act=video" class="btn red">DOWNLOAD VIDEO</button>
<button formaction="/api/index?act=stiker" class="btn dark">STIKER FOTO (512x512)</button>
<button formaction="/api/index?act=hd" class="btn dark">HD FOTO 2X</button>
</form>
<div style="margin-top:10px;color:#0f0;font-size:12px">{msg}</div>
<p style="margin-top:15px;font-size:10px;color:#555">Status: ONLINE ✅</p>
</div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
@app.route('/api/index', methods=['GET','POST'])
def home():
    act = request.args.get('act')
    if request.method == 'GET' or not act:
        return Response(page("Tempel link / upload foto bos!"), mimetype='text/html')
    
    # STIKER
    if act == 'stiker':
        f = request.files.get('file')
        if not f: return Response(page("Upload foto dulu bos!"), mimetype='text/html')
        tmp = tempfile.mkdtemp()
        pin = os.path.join(tmp, "in.jpg"); pout = os.path.join(tmp, "stiker.webp")
        f.save(pin)
        im = Image.open(pin).convert("RGBA"); im.thumbnail((512,512))
        bg = Image.new("RGBA",(512,512),(0,0,0,0))
        bg.paste(im, ((512-im.width)//2,(512-im.height)//2))
        bg.save(pout, "WEBP")
        return send_file(pout, as_attachment=True, download_name="haris_stiker.webp")

   
