# Nexora

Nexora adalah sebuah proyek game 2D sederhana yang dibangun menggunakan bahasa pemrograman **Python** dan library **Pygame**. Proyek ini dirancang khusus untuk mengimplementasikan prinsip-prinsip **Pemrograman Berorientasi Objek (OOP)** secara mendalam dalam skenario pengembangan perangkat lunak nyata.

## 👥 Anggota Kelompok
- M. Ghazwan Caesaryan (25051204097) a.s Game Designer
- Ahmad Zhaura Akbar (25051204237) a.s Game Designer
- Izad Emil Laahut (25051204147) a.s Game Assets
- M. Ersandi (25051204210) a.s Game Audio

## 🚀 Fitur Utama

- **Implementasi OOP Komprehensif:** Menggunakan konsep Class, Inheritance (Pewarisan), Abstraction (Abstraksi), Polymorphism (Polimorfisme), dan Encapsulation (Enkapsulasi).
- **Sistem Gameplay:**
    - Progresi berbasis Stage.
    - Mekanik pertempuran Boss dengan animasi kematian yang detail.
    - Sistem kamera dinamis yang mengikuti pergerakan pemain.
    - Manajemen nyawa (Lives) dan kesehatan (HP).
- **Sistem Penyimpanan:** Fitur Save dan Load game menggunakan format JSON (mendukung hingga 5 slot penyimpanan).
- **Antarmuka Pengguna (UI):** Dialog cerita (Story box), kredit akhir, dan elemen HUD yang interaktif.

## 💻 Arsitektur Kode

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

## 🧠 Implementasi Konsep Object-Oriented Programming (OOP)

Game **Nexora** dikembangkan menggunakan pendekatan **Object-Oriented Programming (OOP)** untuk menciptakan struktur kode yang lebih terorganisir, modular, dan mudah dikembangkan. Dengan menerapkan konsep OOP, setiap komponen dalam game dapat dipisahkan berdasarkan tanggung jawabnya masing-masing sehingga mempermudah pengelolaan kode, pengembangan fitur baru, serta proses debugging. Dalam proyek ini, implementasi OOP diterapkan melalui konsep **Class dan Object**, serta empat pilar utama yaitu **Inheritance**, **Encapsulation**, **Polymorphism**, dan **Abstraction**.

### 🔹 Class dan Object

Konsep dasar OOP yang paling utama adalah **Class** dan **Object**. Dalam pengembangan game **Nexora**, seluruh elemen permainan dirancang menggunakan sistem berbasis objek agar setiap komponen memiliki peran dan perilaku yang jelas.

**Class** berfungsi sebagai blueprint atau cetakan untuk mendefinisikan atribut (data) dan metode (perilaku) suatu entitas dalam game. Sementara itu, **Object** merupakan implementasi nyata dari class yang digunakan saat permainan dijalankan.

Sebagai contoh, class `Player` digunakan untuk merepresentasikan karakter utama yang dimainkan pengguna. Class ini memiliki atribut seperti posisi karakter, jumlah HP, nyawa, kecepatan, dan sistem senjata. Ketika game dimulai, object dari class `Player` akan dibuat sehingga karakter dapat bergerak, menyerang musuh, menerima damage, serta berinteraksi dengan lingkungan permainan.

Selain itu, sistem musuh juga dibangun menggunakan pendekatan class dan object, seperti `NormalEnemy`, `DroneEnemy`, `PlaneEnemy`, `TankEnemy`, hingga `BossEnemy`. Setiap class memiliki perilaku yang berbeda, namun tetap mengikuti struktur dasar yang telah ditentukan. Dengan pendekatan ini, sistem game menjadi lebih fleksibel dan mudah dikembangkan.

### 🔹 Inheritance (Pewarisan)

Konsep **Inheritance** diterapkan untuk menciptakan hubungan hierarki antar class sehingga atribut dan metode dapat diwariskan dari class induk (**superclass**) ke class turunan (**subclass**). Penerapan inheritance membantu mengurangi duplikasi kode serta membuat struktur program lebih efisien.

Pada proyek **Nexora**, class `Character` digunakan sebagai superclass utama yang diwariskan kepada berbagai subclass seperti `Player`, `Bullet`, dan sistem musuh. Selain itu, terdapat class `BaseEnemy` yang menjadi dasar bagi berbagai jenis musuh seperti `NormalEnemy`, `PlaneEnemy`, `DroneEnemy`, `TankEnemy`, dan `BossEnemy`.

Melalui inheritance, seluruh entitas dapat berbagi fungsi umum seperti sistem pergerakan, gravitasi, maupun status aktif tanpa perlu menulis ulang kode yang sama pada setiap class. Namun demikian, masing-masing subclass tetap dapat memiliki perilaku unik sesuai kebutuhan gameplay.

### 🔹 Encapsulation (Enkapsulasi)

**Encapsulation** diterapkan untuk menjaga keamanan data penting dalam sistem permainan dengan membatasi akses langsung terhadap atribut tertentu. Data internal suatu object tidak dapat diubah sembarangan dari luar class, melainkan harus melalui metode yang telah disediakan.

Dalam game **Nexora**, atribut penting pemain seperti **Health Point (HP)** dan **jumlah nyawa (Lives)** disimpan menggunakan atribut private seperti `__hp` dan `__lives`. Untuk mengakses maupun memodifikasi nilai tersebut, sistem menggunakan metode **getter** dan **setter**, seperti `get_hp()`, `set_hp()`, `get_lives()`, dan `set_lives()`.

Penerapan encapsulation membantu menjaga integritas data permainan sehingga perubahan nilai penting tidak terjadi secara tidak terkontrol. Hal ini juga meminimalkan potensi bug yang dapat memengaruhi keseimbangan gameplay.

### 🔹 Polymorphism (Polimorfisme)

Konsep **Polymorphism** memungkinkan objek dari class yang berbeda menggunakan metode dengan nama yang sama namun menghasilkan perilaku yang berbeda sesuai implementasinya masing-masing.

Pada proyek **Nexora**, polymorphism diterapkan melalui metode `update()` yang dimiliki oleh berbagai jenis musuh. Walaupun semua musuh memiliki method dengan nama yang sama, setiap subclass mengimplementasikan logika yang berbeda.

Sebagai contoh, `DroneEnemy` memiliki pola pergerakan udara yang berbeda dengan `TankEnemy` yang bergerak di darat, sedangkan `BossEnemy` memiliki mekanisme pertarungan kompleks dengan beberapa fase serangan. Meski demikian, sistem game tetap dapat mengelola seluruh musuh dengan satu alur pemanggilan metode yang sama.

Penerapan polymorphism membuat kode menjadi lebih fleksibel dan efisien karena tidak diperlukan logika terpisah untuk setiap jenis musuh.

### 🔹 Abstraction (Abstraksi)

**Abstraction** diterapkan untuk menyederhanakan kompleksitas program dengan menyediakan struktur dasar yang hanya menampilkan fungsi penting kepada subclass, sementara detail implementasi internal disembunyikan.

Dalam proyek ini, abstraction diterapkan menggunakan **Abstract Class** melalui class `Character`. Class ini berfungsi sebagai dasar bagi seluruh entitas bergerak di dalam game dan menyediakan atribut serta fungsi umum seperti sistem pergerakan.

Selain itu, metode `update()` dideklarasikan sebagai metode abstrak sehingga setiap subclass diwajibkan mengimplementasikan perilaku masing-masing. Pendekatan ini memastikan seluruh entitas memiliki struktur yang konsisten namun tetap fleksibel dalam implementasinya.

### 🎯 Kesimpulan Implementasi OOP

Penerapan konsep **Object-Oriented Programming (OOP)** pada game **Nexora** berhasil menciptakan sistem yang lebih modular, terstruktur, dan mudah dikembangkan. Penggunaan **Class dan Object**, serta penerapan **Inheritance**, **Encapsulation**, **Polymorphism**, dan **Abstraction**, memungkinkan pengembangan fitur game dilakukan secara lebih efisien.

Melalui pendekatan ini, berbagai sistem kompleks seperti mekanisme musuh, sistem senjata, save/load game, collision detection, hingga state management dapat diimplementasikan dengan lebih rapi, terorganisir, dan minim redundansi kode.

