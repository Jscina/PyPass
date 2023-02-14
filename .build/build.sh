#!/bin/bash
# Generates the project structure:
#app/
#    app.py
#    templates/
#        index.html
#    static/
#        css/
#            styles.css
#        js/
#            script.js
mkdir app
touch app/app.py
mkdir app/templates
touch app/templates/index.html
mkdir app/static
mkdir app/static/css
touch app/static/css/styles.css
mkdir app/static/js
touch app/static/js/script.js



# Then places sample code inside the files
echo "from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)" > app/app.py

echo "<!DOCTYPE html>
<html>
<head>
    <title>My Flask App</title>
    <link rel='stylesheet' href='{{ url_for('static', filename='css/styles.css') }}'>
</head>
<body>
    <h1>Welcome to my Flask App!</h1>
</body>
</html>" > app/templates/index.html

echo "body {
    background-color: powderblue;
}" > app/static/css/styles.css

echo "console.log('JavaScript is running!')" > app/static/js/script.js
