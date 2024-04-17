from flask import Flask, render_template, request
from finance_info import queryStockInfo, getCurrentTime
# import dotenv

app = Flask('__name__')

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    current_time = None
    if request.method == 'POST':
        current_time = getCurrentTime()
        symbol = request.form.get('symbol',type=str)
        result = queryStockInfo(symbol=symbol)
        if isinstance(result, str):
            return render_template('quote_error.html', result=result)
    return render_template('quote.html', result=result, current_time=current_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)