from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    return '''
    <html><body>
    <a href="/hello_world"> Hello</a> World
    '''

@app.route('/hello_world')
def hello2():
	return '''
	<html><body>
	Hello World
	'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)