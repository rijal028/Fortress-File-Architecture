# Fortress CDR – Zona Aman

**Versi:** v1.1.9 – STRICT Clean Image Rendering Only  
**Status:** Final Prototipe  
**Zona:** Aman (bebas malware, siap dipakai oleh pengguna umum)

---

## 🔰 Tujuan
Fortress CDR – Zona Aman adalah modul pembersih PDF (Content Disarm and Reconstruction / CDR) yang dirancang untuk menghapus seluruh komponen berbahaya dalam file PDF **tanpa kompromi**, khususnya:

- Menghapus **JavaScript otomatis**
- Membersihkan **metadata tersembunyi**
- Menghapus **font, file, form, dan skrip tersembunyi**
- Hanya merender ulang **gambar yang benar-benar aman dari awal** (yang tidak pernah mengandung skrip)

---

## 🧪 Jenis Ancaman yang Dikenali
Berikut adalah ancaman yang secara eksplisit dihapus:

| Ancaman                       | Status Penanganan |
|------------------------------|--------------------|
| JavaScript `/OpenAction`     | ✅ Dihapus          |
| Metadata eksploitatif        | ✅ Dihapus total    |
| Tautan mencurigakan          | ✅ Disaring         |
| Embedded file                | ✅ Dideteksi        |
| Embedded font                | ✅ Dideteksi        |
| Form dinamis (XFA)           | ✅ Dideteksi        |
| Tanda tangan digital         | ✅ Dihitung namun disimpan |
| Gambar mengandung skrip      | ✅ **Tidak dirender** |
| Stream `eval()`, `<script>`  | ✅ Dihapus          |

---

## ⚙️ Fitur Utama

- ✅ Hanya menyalin teks asli dari file
- ✅ Gambar hanya dipertahankan jika **tidak pernah mengandung skrip**
- ✅ Menyimpan tanda tangan digital (opsional)
- ✅ Proses dilakukan secara **lokal** tanpa koneksi internet
- ✅ Output PDF aman, bersih, dan dapat dibaca siapa pun

---

## 📁 Struktur Folder

```
fortress_cdr_zona_aman/
├── README.md
├── fortress_cdr_strict.ipynb    ← Notebook Colab utama
├── requirements.txt             ← Dependensi Python
└── sample_virus_files/          ← (Opsional) File uji coba
```

---

## 🛠️ Cara Menggunakan di Google Colab

1. Buka file `fortress_cdr_strict.ipynb` di Google Colab.
2. Upload file PDF yang ingin diuji.
3. Sistem akan secara otomatis membersihkan ancaman.
4. File hasil akan terdownload secara otomatis sebagai `final_cleaned.pdf`.

---

## 📦 Dependensi

Tambahkan ini ke `requirements.txt` jika ingin dijalankan di lokal:
```txt
pikepdf==9.9.0
reportlab==4.4.2
pymupdf==1.26.3
Pillow>=10.0.1
lxml>=4.8
```

---

## 📌 Catatan Keamanan

- Jika gambar dalam file PDF **pernah mengandung skrip**, maka gambar tersebut **tidak akan dirender ulang sama sekali**, meskipun sudah dibersihkan.
- Tujuan zona ini adalah **non-kompromi**: keamanan diutamakan di atas estetika.

---

## 🧠 Cocok Digunakan Oleh

- Guru, dosen, atau tenaga pendidikan
- Pengguna awam yang menerima dokumen dari pihak tak dikenal
- Institusi yang ingin memastikan file PDF tidak membawa skrip tersembunyi

---

## 📬 Kontak & Kontribusi

Repositori oleh: [@rijal028](https://github.com/rijal028)  
Masukan dan kontribusi sangat diterima. Fork & bintang sangat membantu proyek ini terus berkembang ✨

