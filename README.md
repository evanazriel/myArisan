# 🏛️ myArisan

**myArisan** adalah aplikasi web modern berbasis Django dan PostgreSQL yang dirancang khusus untuk memudahkan kelompok arisan dalam mengelola iuran, pencatatan pengeluaran kas, serta manajemen data anggota secara transparan dan aman dengan sistem multi-tenancy (*data isolation*).

---

## ✨ Fitur Utama

- **🔐 Multi-Tenancy (Data Isolation)**: Setiap akun pengguna memiliki akses data yang terisolasi secara aman, memastikan informasi keuangan antar pengguna tidak saling bercampur.
- **👥 Manajemen Anggota & Sumber Pemasukan**: Kelola daftar nama anggota arisan secara fleksibel per akun.
- **💰 Pencatatan Keuangan (Income & Expense)**: Catat pemasukan iuran dan pengeluaran kas secara terstruktur lengkap dengan nominal, deskripsi, kategori, serta tanggal transaksi.
- **📊 Dashboard Keuangan**: Ringkasan saldo total (pemasukan, pengeluaran, dan sisa uang) yang disajikan secara informatif.
- **🎡 Fitur Spin Wheel Undian**: Dilengkapi fitur roda undian interaktif untuk menentukan pemenang arisan secara adil dan transparan.
- **🌓 Theme Toggle (Light/Dark Mode)**: Antarmuka modern yang dibangun menggunakan Bootstrap 5, mendukung mode terang dan gelap dengan transisi yang mulus.

---

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python, Django Framework
- **Database**: PostgreSQL
- **Dependency Management**: Pipenv
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Version Control**: Git & GitHub

---

## ⚙️ Cara Instalasi & Menjalankan Proyek

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek secara lokal di komputer Anda:

1. **Clone repository ini:**
   ```bash
   git clone [https://github.com/username/myarisan.git](https://github.com/username/myarisan.git)
   cd myarisan

2. **Install Dependensi Menggunakan Pipenv**
   ```bash
    pipenv install

3. **Aktifkan Virtual Enviroment**
   ```bash
    pipenv shell

4. **konfigurasi Enviroment variable**
    Buat file baru bernama .env di dalam folder utama proyek (sejajar dengan file manage.py).
   ```bash
    SECRET_KEY=django-insecure-ganti-dengan-secret-key-anda
    DEBUG=True
    DB_NAME=nama_database_anda
    DB_USER=postgres
    DB_PASSWORD=password_lokal_anda
    DB_HOST=localhost
    DB_PORT=5432

5. **Jalankan Migrasi Database**
   ```bash
    pipenv manage.py makemigrations
    pipenv manage.py migrate

6. 5. **Jalankan server lokal**
   ```bash
    pipenv python manage.py runserver
