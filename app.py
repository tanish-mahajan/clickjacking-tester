from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tsecurity Clickjacking Tester</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input[type=text] {
            padding: 8px;
            width: 300px;
            font-size: 16px;
        }
        button {
            padding: 8px 16px;
            font-size: 16px;
        }
        iframe {
            margin-top: 20px;
            border: 2px solid red;
        }
        .error {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h2>🔒 Tsecurity Clickjacking Test Tool</h2>
    <form method="GET">
        <input type="text" name="url" placeholder="Enter site (e.g. example.com)" value="{{ user_input or '' }}" required />
        <button type="submit">Check</button>
    </form>

    {% if error %}
        <p class="error">❌ Not Working: {{ error }}</p>
    {% elif url %}
        <h3>✅ Framing: {{ url }}</h3>
        <iframe src="{{ url }}" width="100%" height="500px"></iframe>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    user_input = request.args.get("url", "").strip()
    url = None
    error = None

    if user_input:
        # Add scheme if missing
        if not user_input.startswith("http"):
            url = "https://" + user_input
        else:
            url = user_input

        try:
            # Check headers
            resp = requests.head(url, timeout=5, allow_redirects=True)
            headers = resp.headers

            xfo = headers.get("X-Frame-Options", "").lower()
            csp = headers.get("Content-Security-Policy", "").lower()

            if "deny" in xfo or "sameorigin" in xfo or "frame-ancestors" in csp:
                error = "Site is protected with security headers"
                url = None  # Don't embed if protected

        except Exception as e:
            error = f"Could not reach site: {e}"
            url = None

    return render_template_string(HTML_TEMPLATE, url=url, error=error, user_input=user_input)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

