from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('dashboard.html')

# @app.route('/x')
# def showSignUp():
#     return "Welcome!!!"

if __name__ == "__main__":
    app.run()