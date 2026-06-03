# Nexora

Nexora adalah sebuah proyek game 2D sederhana yang dibangun menggunakan bahasa pemrograman **Python** dan library **Pygame**. Proyek ini dirancang khusus untuk mengimplementasikan prinsip-prinsip **Pemrograman Berorientasi Objek (OOP)** secara mendalam dalam skenario pengembangan perangkat lunak nyata.

## 🚀 Fitur Utama

- **Implementasi OOP Komprehensif:** Menggunakan konsep Class, Inheritance (Pewarisan), Abstraction (Abstraksi), Polymorphism (Polimorfisme), dan Encapsulation (Enkapsulasi).
- **Sistem Gameplay:**
    - Progresi berbasis Stage.
    - Mekanik pertempuran Boss dengan animasi kematian yang detail.
    - Sistem kamera dinamis yang mengikuti pergerakan pemain.
    - Manajemen nyawa (Lives) dan kesehatan (HP).
- **Sistem Penyimpanan:** Fitur Save dan Load game menggunakan format JSON (mendukung hingga 5 slot penyimpanan).
- **Antarmuka Pengguna (UI):** Dialog cerita (Story box), kredit akhir, dan elemen HUD yang interaktif.

## 🏗️ Arsitektur Kode

Proyek ini dibagi menjadi beberapa modul untuk menjaga struktur kode tetap rapi dan modular:

- **`main.py`**: Titik masuk utama (entry point) aplikasi yang menjalankan loop permainan.
- **`settings.py`**: Berisi konfigurasi global seperti resolusi layar (`WIDTH`, `HEIGHT`) dan `FPS`.
- **`game.py`**: Inti dari logika permainan, mengelola transisi antar state (Menu, Play, Boss, dsb), serta menangani UI.
- **`world.py`**: Mengelola sistem lingkungan, termasuk *heightmap* untuk pijakan tanah dan pergerakan kamera.
- **`player.py`**: Mendefinisikan kelas `Player`, kontrol pergerakan, sistem HP, dan manajemen senjata.
- **`enemy.py`**: Implementasi berbagai jenis musuh (Normal, Tank, Plane, Drone, Boss) menggunakan konsep *Inheritance*.
- **`entities.py`**: Mengelola objek tambahan di dalam game seperti `MysteryBox`, `Explosion`, dan `EnergyItem`.
- **`utils.py`**: Fungsi pembantu (utility) untuk memuat aset gambar, suara, dan font secara aman.
- **`assets/`**: Direktori penyimpanan aset visual (sprites, UI, maps) dan audio.

## 🛠️ Teknologi yang Digunakan

- **Bahasa:** Python 3.12.7
- **Library Utama:** Pygame
- **Library Tambahan:** Pillow (PIL) - *digunakan untuk pemrosesan dan manipulasi aset gambar*
- **Format Data:** JSON (untuk Save Game)

## 🎮 Cara Menjalankan

1. Pastikan Anda telah menginstal Python di sistem Anda.
2. Instal library Pygame dan Pillow melalui pip:
   ```bash
   pip install pygame Pillow

## 🎮 Cara Menjalankan

Jika Anda belum pernah menjalankan program Python sebelumnya, ikuti langkah-langkah detail berikut:

1. **Unduh dan Instal Python:**
   - Kunjungi situs resmi [python.org](https://www.python.org/downloads/) dan unduh versi terbaru.
   - **PENTING:** Saat proses instalasi di Windows, pastikan Anda mencentang kotak **"Add Python to PATH"** di bagian bawah sebelum menekan "Install Now".

2. **Siapkan Folder Game:**
   - Unduh atau *clone* proyek game ini.
   - Ekstrak file ZIP-nya jika Anda mengunduhnya dalam bentuk ZIP.

3. **Buka Terminal / Command Prompt:**
   - Buka folder game "Nexora" yang sudah diekstrak.
   - Klik pada *address bar* (jalur folder) di bagian atas File Explorer, ketik `cmd`, lalu tekan `Enter`. Ini akan membuka jendela hitam (Command Prompt) yang sudah berada di folder game.

4. **Instal Persyaratan Sistem:**
   - Di jendela hitam tersebut, ketik perintah berikut dan tekan `Enter`:
     ```bash
     pip install pygame Pillow
     ```
   - Tunggu hingga proses pengunduhan selesai.

5. **Mainkan Game:**
   - Setelah instalasi selesai, ketik perintah ini dan tekan `Enter` untuk memulai petualangan Anda:
     ```bash
     python main.py
     ```
