# -*- coding: utf-8 -*-

from flask import Flask, request, json, Response, render_template

app = Flask(__name__)

@app.route("/hello")
@app.route("/hello/<text>")
def hello(text=None):
    #return str(request.args)
    some_list = ['no-no-no','go away','caution']
    return render_template("index.html",text=text, li=some_list),201#, mimetype="text/plain")


@app.route("/")
def index():
    return json.jsonify({'a':request.args.get('a')})

if __name__ == "__main__":
    app.run(debug=True)
