from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    response = request.form['response']
    comment = request.form['comment']

    # Perform any actions with the form data (e.g., store in a database)
    # For now, just print the data to the console
    print(f"Response: {response}, Comment: {comment}")

    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
