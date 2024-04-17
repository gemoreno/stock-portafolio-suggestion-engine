from flask import Flask, request, render_template, redirect, url_for
from finance_info import allocateFunds, queryStockInfoMultiple
# import dotenv

app = Flask('__name__')

@app.route('/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        strategies = request.form.getlist('strategies[]', type=str)
        investment_amount = int(request.form.get('investment_amount', 0))
        if len(strategies) > 0:
            return redirect(url_for('display_portafolio', strategies=",".join(strategies), investment_amount=investment_amount))
    return render_template('home.html')


@app.route('/portafolio/', methods=['GET'])
def display_portafolio():
    strategies = request.args.get('strategies', type=str).split(',')
    investment_amount = request.args.get('investment_amount', type=int)
    
    stocks_info_from_api = queryStockInfoMultiple(strategies=strategies)
    stocks_info_with_allocation = allocateFunds(investment_amount, stocks_info_from_api)
    
    return render_template('portafolio.html', stocks_info=stocks_info_with_allocation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)