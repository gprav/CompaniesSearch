from flask import Flask, request
from flask.templating import render_template
from search import check_postcode, correct_format, search
app = Flask(__name__)

@app.route('/')
def enter_postcode():
    return render_template('enter_postcode.html')

@app.route('/companies',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form['pc']
        valid_postcode = check_postcode(result)
        if valid_postcode == False:
            error = "Invalid postcode. Please enter postcode again."
            return render_template('enter_postcode.html', error = error)
        result = correct_format(result)
        rows, previous_month3, previous_month = search(result)
        str_previous_month3 = previous_month3.strftime("%B %Y")
        str_previous_month = previous_month.strftime("%B %Y")
        if len(result) == 7:
            postcode = result[0:3]
        else:
            postcode = result[0:4]
        return render_template('result.html', rows=rows, previous_month3=str_previous_month3, previous_month=str_previous_month, postcode=postcode, count=len(rows))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
