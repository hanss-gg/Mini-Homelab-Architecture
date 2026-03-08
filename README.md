# Mini-Homelab-Architecture

## Overview

This project demonstrates a simple cloud-style architecture built locally using virtual machines.
The environment simulates a common application deployment pattern where an application server communicates with a separate database server.

The goal of this homelab is to practice:

* Linux server administration
* Virtual machine networking
* Application deployment
* Database integration
* Basic cloud architecture concepts

The setup is built using **VirtualBox** and **Ubuntu Server**.

---

## Architecture

```
Laptop (Browser / SSH)
        │
        │
        ▼
App Server VM
192.168.56.11
(Flask Application)
        │
        │ PostgreSQL connection
        ▼
DB Server VM
192.168.56.12
(PostgreSQL Database)
```

### Components

| Component         | Role                                                |
| ----------------- | --------------------------------------------------- |
| Laptop            | Client accessing the application via browser or SSH |
| App Server        | Runs the web application                            |
| DB Server         | Hosts the PostgreSQL database                       |
| Host-only Network | Allows communication between VMs                    |

---

## Infrastructure

### Virtualization

* Virtual Machine Platform: Oracle VM VirtualBox
* OS: Ubuntu Server

### Virtual Machines

| VM Name    | Role               | IP Address    |
| ---------- | ------------------ | ------------- |
| app-server | Application server | 192.168.56.11 |
| db-server  | Database server    | 192.168.56.12 |

---

## Network Configuration

Two network interfaces are used on each VM:

### Adapter 1 — NAT

Provides internet access for:

* apt update
* package installation

Example IP:

```
10.0.2.x
```

### Adapter 2 — Host-only

Used for internal communication between VMs.

```
192.168.56.0/24
```

Example:

```
app-server → 192.168.56.11
db-server  → 192.168.56.12
```

---

## Database Setup

Database server runs **PostgreSQL**.

### Installation

```
sudo apt install postgresql postgresql-contrib
```

### Database

```
homelabdb
```

### Database User

```
labuser
```

### Allow Remote Access

Configuration files modified:

```
/etc/postgresql/*/main/postgresql.conf
```

```
listen_addresses = '*'
```

and

```
/etc/postgresql/*/main/pg_hba.conf
```

```
host    homelabdb    labuser    192.168.56.11/32    md5
```

---

## Application Server

A simple web application was deployed using **Flask**.

### Project Structure

```
homelab-app
 ├── app.py
 ├── requirements.txt
 └── venv
```

### Python Dependencies

```
Flask
psycopg2-binary
```

Installed with:

```
pip install flask psycopg2-binary
```

---

## Application Code (Simplified)

The application exposes two endpoints:

### Root Endpoint

```
/
```

Returns:

```
Homelab App Running
```

### Database Endpoint

```
/db
```

Tests connection to PostgreSQL and returns database version.

---

## Running the Application

Activate virtual environment:

```
source venv/bin/activate
```

Start the application:

```
python app.py
```

Application runs on:

```
http://192.168.56.11:5000
```

---

## Example Request Flow

```
Browser
   │
   ▼
Flask App (192.168.56.11)
   │
   ▼
PostgreSQL DB (192.168.56.12)
```

---

## Skills Practiced

This homelab demonstrates practical skills related to:

* Linux server configuration
* VM networking
* SSH administration
* PostgreSQL database setup
* Application deployment
* Service communication across servers

---

## Future Improvements

Planned upgrades for this project:

* Reverse proxy with Nginx
* Run application with Gunicorn
* Containerize the application with Docker
* Infrastructure automation
* CI/CD pipeline

---

## Author

Student homelab project for learning cloud and DevOps concepts.
