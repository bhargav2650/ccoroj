from flask import Flask

app = Flask(__name__)
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'
 
# main driver function
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')