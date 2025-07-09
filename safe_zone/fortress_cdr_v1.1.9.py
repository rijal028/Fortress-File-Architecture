# Fortress CDR v1.1.9 – STRICT Clean Image Rendering using Object Lineage Filtering

import pikepdf, fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from google.colab import files
from urllib.parse import urlparse
import re, io, os

# === Upload File ===
uploaded = files.upload()
input_file = list(uploaded.keys())[0]
print(f"🗵️ File diterima: {input_file}")
log = []

# === Domain whitelist ===
whitelist = [
    "google.com", "youtube.com", "github.com", "scholar.google.com",
    "kemdikbud.go.id", "unpad.ac.id", "umn.ac.id"
]
def link_aman(url):
    try:
        domain = urlparse(url).netloc.lower().replace("www.", "")
        return any(d in domain for d in whitelist)
    except: return False

# === 1. Hapus JavaScript ===
with pikepdf.open(input_file, allow_overwriting_input=True) as pdf:
    root = pdf.trailer["/Root"]
    if "/OpenAction" in root:
        log.append("[CDR] JavaScript ditemukan di /OpenAction.")
        del root["/OpenAction"]
        log.append("[CDR] /OpenAction telah dihapus.")
    pdf.save("fortress_clean.pdf")

# === 2. Logging metadata ===
with pikepdf.open("fortress_clean.pdf") as pdf:
    for k, v in pdf.docinfo.items():
        log.append(f"[CDR] Metadata ditemukan: {k} = {v}")

# === 3. Hapus metadata ===
with pikepdf.open("fortress_clean.pdf", allow_overwriting_input=True) as pdf:
    pdf.docinfo = pdf.make_indirect(pikepdf.Dictionary())
    pdf.save("fortress_clean.pdf")

# === 4–6. Font, embedded file, XFA/Signature ===
with fitz.open("fortress_clean.pdf") as doc:
    for i, page in enumerate(doc, 1):
        for f in page.get_fonts(full=True):
            if f[5]:
                log.append(f"[CDR] Embedded font '{f[3]}' ditemukan di halaman {i}")

with pikepdf.open("fortress_clean.pdf") as pdf:
    if "/EmbeddedFiles" in pdf.trailer["/Root"].get("/Names", {}):
        log.append("[CDR] Embedded file ditemukan di /Names -> /EmbeddedFiles")
    acroform = pdf.trailer["/Root"].get("/AcroForm", {})
    if acroform:
        if "/XFA" in acroform:
            log.append("[CDR] Form dinamis (XFA/XML) terdeteksi di struktur PDF (/AcroForm -> /XFA)")
        else:
            log.append("[CDR] Struktur form PDF ditemukan di /AcroForm (statis, non-XFA)")
        for field in acroform.get("/Fields", []):
            try:
                if field.get_object().get("/FT") == "/Sig":
                    log.append("[CDR] Tanda tangan digital terdeteksi di /AcroForm -> /Fields -> /Sig")
            except: continue

# === 7. Deteksi objgen dari stream mencurigakan ===
suspicious = [b'javascript', b'app.alert', b'openaction', b'/embeddedfile', b'xfa',
              b'<script', b'eval(', b'cod.exe', b'powershell', b'payload']
objgen_berbahaya = set()

with pikepdf.open(input_file) as pdf:
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream):
            try:
                raw = obj.read_bytes().lower()
                if any(p in raw for p in suspicious):
                    objgen_berbahaya.add(obj.objgen)
                    log.append(f"[CDR] Stream mencurigakan ditemukan di objek {obj.objgen}")
            except: continue

# === 8. Ekstrak teks & gambar aman berdasarkan objgen lineage ===
doc = fitz.open(input_file)
extracted_text = ""
gambar_aman = []

for p in range(len(doc)):
    page = doc[p]
    extracted_text += page.get_text()
    for img in page.get_images(full=True):
        xref = img[0]
        obj = doc.xref_object(xref, compressed=False)
        # ambil objgen dari informasi xref line
        match = re.match(r"(\d+)\s(\d+)\sobj", obj)
        if match:
            objnum = int(match.group(1))
            gen = int(match.group(2))
            if (objnum, gen) not in objgen_berbahaya:
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5:
                        path = f"safe_img_{p}_{xref}.png"
                        pix.save(path)
                        gambar_aman.append((p, path))
                except Exception as e:
                    log.append(f"[CDR] Gagal merender gambar objek {xref} di halaman {p+1}: {str(e)}")
            else:
                log.append(f"[CDR] Gambar xref {xref} di halaman {p+1} tidak dirender karena berasal dari objgen berbahaya.")

# === 9. Teks mencurigakan ===
for keyword in ["app.alert", "<script", "eval(", "iframe", "onload=", "onclick="]:
    if keyword.lower() in extracted_text.lower():
        log.append(f"[CDR] Teks mencurigakan ditemukan: '{keyword}'")

# === 10. Bangun ulang PDF ===
packet = io.BytesIO()
c = canvas.Canvas(packet, pagesize=letter)
w, h = letter
y = h - 40
img_iter = iter(gambar_aman)
hal = 0

for line in extracted_text.split("\n"):
    if y < 100:
        c.showPage()
        y = h - 40
        hal += 1
    while True:
        try:
            pg, path = next(img_iter)
            if pg == hal:
                c.drawImage(path, 40, y - 80, width=120, height=80)
                y -= 100
                continue
            else:
                img_iter = (i for i in [(pg, path)] + list(img_iter))
                break
        except StopIteration:
            break
    for u in re.findall(r"http[s]?://\S+", line):
        if not link_aman(u):
            log.append(f"[CDR] Tautan mencurigakan telah dihapus: {u}")
            line = line.replace(u, "[TAUTAN DIHAPUS]")
    c.drawString(40, y, line)
    y -= 15

c.save()
packet.seek(0)

# === 11. Simpan akhir ===
with open("final_cleaned.pdf", "wb") as f:
    f.write(packet.read())

# === 12. Log ===
print("\n=== LOG FORTRESS CDR FINAL ===")
if log:
    for l in log: print(l)
    print("📌 Semua ancaman telah ditangani.")
else:
    print("✅ Tidak ditemukan ancaman.")
files.download("final_cleaned.pdf")

# === 13. Bersihkan cache gambar ===
for _, path in gambar_aman:
    if os.path.exists(path): os.remove(path)
