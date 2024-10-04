from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello from Flask!'

if __name__ == '__main__':
  app.run()

@app.route('/countme/<input_str>')
def count_me(input_str):
    return input_str
