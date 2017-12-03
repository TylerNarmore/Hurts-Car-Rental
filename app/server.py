from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/inventory.html')
def inventory():
    return render_template('inventory.html')



@app.route('/christmas')
def christmas():
    return """
    <html>    
        <body>
            <center><h1>Happy Holidays from the Software Bois</h1></center>
            <img src="/static/imgs/ChristmasCard.png" alt="Christmas Bois" style="max-width:100%;max-height=100%">
        </body>
    </html>
    """

def main():
    app.run(host="0.0.0.0", debug=True)