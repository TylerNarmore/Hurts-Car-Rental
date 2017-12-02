from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/christmas')
def christmas():
    return """
    <html>    
        <body>
            <h1>Happy Holidays from the Software Bois</h1>
            <img src="imgs/ChristmasCard" alt="Christmas Bois" style="max-width:100%;max-height=100%">
        </body>
    </html>
    """

def main():
    app.run(host="0.0.0.0", debug=True)