from flask import Flask, render_template, request
from bsedata.bse import BSE

app = Flask(__name__)

b = BSE()

# Stocks With Their Company Code
stocks = {
    "Symphony Limited": {
        "code": "517385",
        "price": 991,
        "quantity": 1
    },
    "Restaurant Brands Asia Ltd": {
        "code": "543248",
        "price": 100.09,
        "quantity": 16
    },
    "RELIANCE POWER LTD": {
        "code": "532939",
        "price": 12.47,
        "quantity": 173
    },
    "Jaiprakash Power Ventures Limited": {
        "code": "532627",
        "price": 5.82,
        "quantity": 600
    },
    "PAYTM": {
        "code": "543396",
        "price": 643.05,
        "quantity": 8
    },
    "IIFL Finance Ltd": {
        "code": "532636",
        "price": 484.05,
        "quantity": 14
    },
    "Sula Vineyards Ltd": {
        "code": "543711",
        "price": 380.40,
        "quantity": 20
    },
    "Adani Green Energy Ltd": {
        "code": "541450",
        "price": 912.12,
        "quantity": 11
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock = request.form['stock']
        purchase_price = float(request.form['purchase_price'])
        quantity = int(request.form['quantity'])

        stocks[stock] = {
            "code": stock,
            "price": purchase_price,
            "quantity": quantity
        }

    stock_data = []

    total_invested_amount = 0
    total_current_amount = 0

    for stock, details in stocks.items():
        code = details["code"]
        purchase_price = details["price"]
        quantity = details["quantity"]

        quote = b.getQuote(code)
        current_price = float(quote["currentValue"])

        if current_price > purchase_price:
            profit = int((current_price - purchase_price) * quantity * 1.5)
            color = "green"
            status = f"Profit: {profit}"
        elif current_price == purchase_price:
            color = "black"
            status = "No Profit No Loss"
        else:
            loss = int((purchase_price - current_price) * quantity)
            color = "red"
            status = f"Loss: {loss}"

        invested_amount = purchase_price * quantity
        current_amount = current_price * quantity

        total_invested_amount += invested_amount
        total_current_amount += current_amount

        stock_data.append({
            "stock": stock,
            "purchase_price": purchase_price,
            "quantity": quantity,
            "current_price": current_price,
            "status": status,
            "color": color,
            "invested_amount": invested_amount,
            "current_amount": current_amount
        })

    return render_template('stock_information.html', stocks=stock_data, total_invested_amount=total_invested_amount, total_current_amount=total_current_amount)

if __name__ == '__main__':
    app.run()