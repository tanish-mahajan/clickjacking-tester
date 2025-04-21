# 🔒 Tsecurity Clickjacking Tester

A simple Python Flask app to test whether a website is vulnerable to **clickjacking** by attempting to load it in an `<iframe>` and checking for security headers like `X-Frame-Options` and `Content-Security-Policy`.

---

## 🚀 How to Use

### 🔧 Requirements

- Python 3
- Flask
- `requests` library

Install dependencies:

```bash
pip install flask requests
```

## ▶️ Run the App
Run the app with:
```bash
sudo python3 app.py
```
Note: The app runs on port 80. If you don’t want to use sudo or need a different port, change the port=80 in the code.

## 🌐 Access in Browser
Once the app is running, open your browser and navigate to:
```bash
http://localhost/
```
Or if accessing from another device on the same network:
```bash
http://<your-local-ip>/
```
## 🧪 How It Works
1. Enter a domain like example.com or a full URL like https://example.com.
2. The app will:
  * Send a HEAD request to fetch response headers.
  * Check for the presence of X-Frame-Options or Content-Security-Policy.
  * Try to load the site in an <iframe>.
3. If no protection headers are found, the site will load in the iframe, indicating it's vulnerable to clickjacking.

## ⬇️ Download POC
* If a website is vulnerable to clickjacking and is loading in the iframe, then you can download it's POC with ⬇️ Download PoC HTML button and send to company.
* ⬇️ Download PoC HTML Button is only available when website is loading in iframe.
* 
## ✅ Result Logic
1. If the iframe loads, the site is likely vulnerable to clickjacking.
2. If blocked with a message like "Not Working: Site is protected with security headers," it means the site is protected by:

* X-Frame-Options: DENY/SAMEORIGIN
* Content-Security-Policy: frame-ancestors

## 📄 License

This project is licensed under the MIT License.  
© 2025 Tsecurity
