from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return 'About!'


if __name__ == '__main':
    app.run(debug=True)