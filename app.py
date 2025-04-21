from flask import Flask, render_template_string, request, make_response
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Clickjacking Tester</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input[type=text], button { padding: 8px; font-size: 16px; }
        iframe { margin-top: 20px; width: 100%; height: 500px; border: 2px solid #555; }
        .error { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h2>🔒 Clickjacking Test Tool</h2>
    <form method="GET">
        <input type="text" name="url" placeholder="Enter site (e.g. example.com)" value="{{ user_input or '' }}" required />
        <button type="submit">Check</button>
    </form>
    {% if error %}
        <p class="error">❌ {{ error }}</p>
    {% elif url %}
        <h3>✅ Framing: {{ url }}</h3>
        <iframe src="{{ url }}"></iframe>
        <form method="POST" action="/download">
            <input type="hidden" name="target" value="{{ url }}">
            <button type="submit">⬇️ Download PoC HTML</button>
        </form>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    user_input = request.args.get("url", "").strip()
    url = None
    error = None

    if user_input:
        if not user_input.startswith("http"):
            url = "https://" + user_input
        else:
            url = user_input

        try:
            resp = requests.head(url, timeout=5, allow_redirects=True)
            headers = resp.headers

            xfo = headers.get("X-Frame-Options", "").lower()
            csp = headers.get("Content-Security-Policy", "").lower()

            if "deny" in xfo or "sameorigin" in xfo or "frame-ancestors" in csp:
                error = "Not Working: Site is protected with security headers"
                url = None
        except Exception as e:
            error = f"Error: {e}"
            url = None

    return render_template_string(HTML, url=url, error=error, user_input=user_input)

@app.route("/download", methods=["POST"])
def download():
    target = request.form.get("target")
    poc_html = f"""<!DOCTYPE html>
<html>
<head><title>Clickjacking PoC</title></head>
<body>
    <h2>Clickjacking PoC for: {target}</h2>
    <iframe src="{target}" width="100%" height="800" style="border:2px solid red;"></iframe>
</body>
</html>
"""
    response = make_response(poc_html)
    response.headers['Content-Disposition'] = 'attachment; filename=clickjacking_poc.html'
    response.mimetype = 'text/html'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
