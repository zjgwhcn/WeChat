from flask import Flask, render_template

app = Flask(__name__)

app.debug = True


@app.route('/inde')
def inde():
    return render_template('index.html')


app.run(host='0.0.0.0', port=5000)
