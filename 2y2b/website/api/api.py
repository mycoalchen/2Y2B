from flask import Flask, request

app = Flask(__name__)

@app.route('/test')
def test_func():
    name = request.args.get('name')
    return {'response': name + ' is bottom g'}