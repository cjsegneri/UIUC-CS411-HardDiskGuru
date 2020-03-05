from flask import Flask, escape, request, render_template


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    #name = request.args.get("name", "Page")
    return render_template('home.html')

@app.route('/about')
def about():
    #name = request.args.get("name", "Page")
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)