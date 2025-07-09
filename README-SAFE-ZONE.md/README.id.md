# 🛡️ Fortress CDR – Zona Aman v1.1.9 (Final Prototype)

**Fortress CDR** adalah sistem pemrosesan ulang file PDF yang dirancang khusus untuk membersihkan berbagai jenis ancaman digital **tanpa kompromi**, mengikuti prinsip keamanan ketat Zona Aman dari Fortress File Architecture.

> 🔒 Tujuan utamanya: menjaga keamanan mutlak bagi pengguna umum—seperti guru, pelajar, dan masyarakat umum—yang hanya perlu membuka atau memeriksa isi PDF **tanpa risiko** tersembunyi.

---

## 🧩 Fitur Utama

- ✅ **Hapus JavaScript aktif** (`/OpenAction`)
- ✅ **Bersihkan metadata berbahaya**
- ✅ **Deteksi & hapus font tertanam**
- ✅ **Isolasi file tertanam (`/EmbeddedFiles`)**
- ✅ **Deteksi form aktif dan tanda tangan digital**
- ✅ **Filter tautan mencurigakan** (berdasarkan whitelist)
- ✅ **Tolak semua gambar yang pernah mengandung skrip berbahaya**
- ✅ **Tidak ada toleransi render ulang dari gambar yang sebelumnya berisiko**

---

## 🧪 Jenis Ancaman yang Diuji

| No | Jenis Ancaman                   | Hasil CDR                   |
|----|----------------------------------|------------------------------|
| 1  | JavaScript aktif (`/OpenAction`) | ✅ Dihapus total             |
| 2  | Metadata eksploitasi             | ✅ Dikosongkan               |
| 3  | Form dinamis (XFA)               | ✅ Terdeteksi & dilaporkan   |
| 4  | Gambar dengan skrip tersembunyi  | ✅ **Tidak dirender ulang**  |
| 5  | Embedded file (file tertanam)    | ✅ Dihapus & dilogging       |
| 6  | Tautan berbahaya                 | ✅ Dihapus & dilogging       |
| 7  | Font tertanam                    | ✅ Terdeteksi & dilogging    |

---

## 🗃️ Struktur Output

Setelah proses CDR selesai:
- File baru: `final_cleaned.pdf`
- Gambar hanya muncul jika **benar-benar bersih dari awal**
- Semua hasil ancaman akan ditulis dalam log di terminal (`=== LOG FORTRESS CDR FINAL ===`)

---

## 🚧 Catatan Penggunaan

- Ini adalah prototipe akhir **Zona Aman**, bukan versi rilis produk.
- Tidak dirancang untuk dokumen interaktif atau digital signage.
- Gambar atau video yang terdeteksi pernah mengandung skrip **akan dihapus total**, sesuai prinsip Zero Tolerance.

---

## 📎 Untuk Pengembang Lain

Skrip ini kompatibel dengan:
- Python 3.11+
- `pikepdf`, `PyMuPDF (fitz)`, `reportlab`, dan `Pillow`
- Disiapkan untuk integrasi modular ke dalam Fortress File Architecture.

---

## 🧠 Tentang Zona Aman

Zona ini tidak mendukung:
- Visual interaktif
- Media aktif (video playable, JS, animasi)
- Tanda tangan digital interaktif

Tetapi cocok untuk:
- Arsip
- Dokumen hukum non-tandatangan
- Penggunaan pendidikan, dan lainnya.

---

> Versi terakhir: `Fortress CDR v1.1.9 – STRICT Clean Image Rendering Only (Final Prototype)`  
> Jika ditemukan bug baru, akan dirilis patch minor terpisah (`v1.1.9a`, `v1.1.9b`, dst).

