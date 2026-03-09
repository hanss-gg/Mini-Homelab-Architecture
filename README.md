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
   ↓
Flask App (192.168.56.11)
   ↓
PostgreSQL (192.168.56.12)
```

---

## Upgrade #1 Reverse Proxy with Nginx

Browser no longer accesses Flask directly at port 5000, but via port 80 like a normal web server.

Install Nginx: 
```
sudo apt update
sudo apt install nginx -y
```

Reverse Proxy Configuration: 
```
sudo nano /etc/nginx/sites-available/flask-app
```
```
server {
    listen 80;

    server_name 192.168.56.11;

    location / {
        proxy_pass http://127.0.0.1:5000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
Activate Configuration: 
```
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
```

Restart Nginx System: 
```
sudo systemctl restart nginx
```

Now App Server run on:
```
http://192.168.56.11
```
Server Architecture (#1):
```
Laptop (browser)
        ↓
   Nginx :80
        ↓
 Flask App :5000
        ↓
 PostgreSQL
```

## Upgrade #2 Run Flask App as a Service with Systemd

Create new service file for flask app: 
```
sudo nano /etc/systemd/system/flask-app.service
```
flask-app.service Configuration: 
```
[Unit]
Description=Flask App Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/app
ExecStart=/usr/bin/python3 /home/ubuntu/app/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Reload Systemd: 
```
sudo systemctl daemon-reload
```

Start the service & Check the status: 
```
sudo systemctl start flask-app
sudo systemctl status flask-app
```

Activate Auto-Start:
```
sudo systemctl enable flask-app
```

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
