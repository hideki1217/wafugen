from flask import Flask

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>HTML Sample</title>
  <link rel="stylesheet" href="style.css">
  <script type="text/javascript" src="sample.js"></script>
</head>
<body>
  <div class="header">Header領域</div>
  <div class="main">
    <h1>見出し</h1>
    <p>コンテンツ</p>
    <img src="img/sample1.jpg">
  </div>
  <div class="footer">
    <span>Footer領域</span>
    <a href="#">リンク</a>
  </div>
</body>
</html>
"""

app.run(port=8080, debug=True)
