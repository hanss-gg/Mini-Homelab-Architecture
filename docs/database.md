# Database Server Setup

Dokumentasi ini menjelaskan konfigurasi database server
yang digunakan oleh aplikasi pada App Server.

Database yang digunakan: PostgreSQL

Server berjalan pada VM terpisah untuk meniru arsitektur
yang umum digunakan pada cloud environment.

---

# Server Information

| Component | Value |
|------|------|
| Server | DB Server VM |
| IP Address | 192.168.56.12 |
| Database | PostgreSQL |
| Port | 5432 |

---

# Install PostgreSQL

Update package repository:

```
sudo apt update
```

Install PostgreSQL:

```
sudo apt install postgresql postgresql-contrib
```

Cek service:

```
sudo systemctl status postgresql
```

---

# Create Database

Masuk ke PostgreSQL:

```
sudo -u postgres psql
```

Create database:

```
CREATE DATABASE homelab;
```

Create user:

```
CREATE USER homelab_user WITH PASSWORD 'password';
```

Grant access:

```
GRANT ALL PRIVILEGES ON DATABASE homelab TO homelab_user;
```

Exit:

```
\q
```

---

# Allow Remote Connection

Edit file:

```
/etc/postgresql/*/main/postgresql.conf
```

Ubah:

```
listen_addresses = '*'
```

---

Edit file:

```
/etc/postgresql/*/main/pg_hba.conf
```

Tambahkan:

```
host    all    all    192.168.56.0/24    md5
```

Restart service:

```
sudo systemctl restart postgresql
```

---

# Connection Test from App Server

Masuk ke App Server lalu jalankan:

```
psql -h 192.168.56.12 -U homelab_user -d homelab
```

Jika berhasil maka App Server sudah dapat terhubung ke database.

---

# Architecture Role

Database server bertugas untuk:

- Menyimpan data aplikasi
- Melayani query dari App Server
- Memisahkan layer aplikasi dan data

---

# Summary

Database server berjalan secara terpisah dari App Server
untuk meningkatkan skalabilitas dan keamanan sistem.
