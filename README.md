
# 🧠 HappyFit - Video Call & Fitness Backend (Django + Agora + EC2 + Nginx)

This project contains the backend server for the HappyFit app, which supports video calling using Agora and a Django-based API system. This README walks through the complete local setup, deployment on AWS EC2, and Nginx configuration.

---

## 📁 Project Structure

```
happyfit/
├── agora/                    # Agora app logic
├── backend/                 # Django project folder
│   └── settings.py
├── templates/               # HTML templates
├── manage.py
├── db.sqlite3
├── .env                     # Secrets (not pushed to GitHub)
├── requirements.txt
└── README.md
```

---

## ✅ Local Setup Instructions (Windows)

### 1. Clone the repo
```bash
git clone https://github.com/your-username/happyfit-video.git
cd happyfit-video
```

### 2. Setup virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```env
SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
AGORA_APP_ID=your-agora-app-id
AGORA_APP_CERTIFICATE=your-agora-app-certificate
```

> ✅ `.env` is ignored via `.gitignore`

### 5. Run server (for development)
```bash
python manage.py runserver
```

### 6. Run server using **waitress** for production-style local test
```bash
pip install waitress
waitress-serve --listen=127.0.0.1:8000 backend.wsgi:application
```

---

## ☁️ EC2 Setup Instructions

### 1. Launch EC2 Instance (Ubuntu 24.04)
- Choose region (e.g., Mumbai)
- Configure inbound rules to allow:
  - SSH (22) from your IP
  - HTTP (80)
  - Custom TCP 8000 (for Django testing)

### 2. SSH into EC2
```bash
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@<public-ip>
```

### 3. Install dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv git nginx -y
```

### 4. Clone repo & setup project
```bash
git clone https://github.com/your-username/happyfit-video.git
cd happyfit-video
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run Django (temp test)
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🌐 NGINX + Gunicorn (on EC2)

> Skip `gunicorn` on Windows. Use it only on EC2 (Linux)

### 1. Install gunicorn
```bash
pip install gunicorn
```

### 2. Test with gunicorn
```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

### 3. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/happyfit
```

Paste this:

```nginx
server {
    listen 80;
    server_name <your-public-ip>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/happyfit /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

Now visit: http://<your-ec2-public-ip>

---

## 🔒 Production Notes
- Never use Django’s dev server in production
- Use Nginx + Gunicorn
- Secure with HTTPS using Certbot
- Add environment variables via `.env` + `python-decouple`

---

## 📦 Deployment Checklist

- [x] Git repo initialized with `.gitignore`
- [x] `.env` excluded from version control
- [x] EC2 instance with security group configured
- [x] Nginx reverse proxy setup
- [x] Token generation working for Agora
- [x] Frontend integrated with Agora SDK

---

## 🙋‍♂️ Troubleshooting

| Issue | Fix |
|------|-----|
| Port 8000 not reachable | Add it to EC2 security group |
| `.env` visible on GitHub | Add `.env` to `.gitignore` |
| Gunicorn error on Windows | Use `waitress` locally |

---

## 👨‍💻 Maintainer
Srivatsava Gade
