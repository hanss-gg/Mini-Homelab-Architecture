# Network Configuration

Dokumentasi ini menjelaskan konfigurasi jaringan pada homelab yang dijalankan menggunakan
**VirtualBox** dengan dua VM server.

Platform virtualisasi yang digunakan:
- Virtualization: : VirtualBox
- OS Server: : Ubuntu Server

---

# Network Topology

Laptop (Host Machine)

↓

App Server VM — 192.168.56.11

↓

DB Server VM — 192.168.56.12

Semua VM berada dalam **Host-Only Network** sehingga dapat saling berkomunikasi
tanpa terhubung langsung ke internet.

---

# VirtualBox Network Settings

## Adapter Configuration

Setiap VM memiliki 2 network adapter:

### Adapter 1 (Internet Access)

Mode:

NAT

Digunakan untuk:
- `apt update`
- `apt install`
- akses internet

---

### Adapter 2 (Internal Communication)

Mode:

Host-only Adapter

Network:

```
vboxnet0
```

IP range:

```
192.168.56.0/24
```

Digunakan untuk komunikasi antar server.

---

# Static IP Configuration

Konfigurasi dilakukan melalui:

```
/etc/netplan/50.cloud-init.yaml
```

Contoh konfigurasi netplan:

```yaml
network:
  version: 2
  ethernets:
    enp0s8:
      addresses:
        - 192.168.56.11/24 #app-server
```

Apply konfigurasi:

```
sudo netplan apply
```

---

# IP Address Allocation

| Machine | IP Address |
|-------|-------|
| Laptop | 192.168.56.1 |
| App Server | 192.168.56.11 |
| DB Server | 192.168.56.12 |

---

# Connectivity Test

### Test ping antar server

```
ping 192.168.56.12
```

### Test ping ke internet

```
ping 8.8.8.8
```

---

# SSH Access

Laptop dapat mengakses server menggunakan SSH:

```
ssh user@192.168.56.11
```

atau

```
ssh user@192.168.56.12
```

---

# HTTP Access

Aplikasi Flask berjalan pada App Server:

```
http://192.168.56.11:5000
```

Browser pada laptop dapat mengakses aplikasi tersebut.

---

# Summary

Network homelab ini menggunakan:

- Host-only network untuk komunikasi antar VM
- NAT adapter untuk akses internet
- Static IP untuk stabilitas komunikasi server
