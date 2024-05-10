from flask import Flask, request, render_template, redirect, url_for
from finance_info import allocateFunds, queryStockInfoMultiple, get_historical_data

app = Flask('__name__')


@app.route('/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        strategies = request.form.getlist('selected_strategies', type=str)
        investment_amount = int(request.form.get('investment_amount', 0))
        if len(strategies) > 0:
            return redirect(
                url_for('display_portafolio', strategies=",".join(strategies), investment_amount=investment_amount))
    return render_template('index.html')


@app.route('/portafolio/', methods=['GET'])
def display_portafolio():
    strategies = request.args.get('strategies', type=str).split(',')
    investment_amount = request.args.get('investment_amount', type=int)

    stocks_info_from_api = queryStockInfoMultiple(strategies=strategies)
    stocks_info_with_allocation = allocateFunds(investment_amount, stocks_info_from_api)
    dates, historical_data_for_stocks = get_historical_data(stocks_info_with_allocation)

    return render_template('Strategies.html', stocks_info=stocks_info_with_allocation,
                           dates=dates, historical_data=historical_data_for_stocks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
