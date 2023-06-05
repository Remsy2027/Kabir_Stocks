from flask import Flask, render_template, request
from bsedata.bse import BSE

app = Flask(__name__)

b = BSE(update_codes=True)  # Update the codes to fetch the latest data

# Stocks With Their Company Code and Average Price
stocks = {
    "Symphony Limited": {
        "code": "517385",
        "price": 991,
        "quantity": 1,
        "average_price": 1143.85
    },
    "Restaurant Brands Asia Ltd": {
        "code": "543248",
        "price": 100.09,
        "quantity": 16,
        "average_price": 174.77
    },
    "RELIANCE POWER LTD": {
        "code": "532939",
        "price": 12.47,
        "quantity": 173,
        "average_price": 18.75
    },
    "Jaiprakash Power Ventures Limited": {
        "code": "532627",
        "price": 5.82,
        "quantity": 600,
        "average_price": 8.30
    },
    "PAYTM": {
        "code": "543396",
        "price": 643.05,
        "quantity": 8,
        "average_price": 743.36
    },
    "IIFL Finance Ltd": {
        "code": "532636",
        "price": 484.05,
        "quantity": 14,
        "average_price": 505
    },
    "Sula Vineyards Ltd": {
        "code": "543711",
        "price": 380.40,
        "quantity": 20,
        "average_price": 424.80
    },
    "Adani Green Energy Ltd": {
        "code": "541450",
        "price": 912.12,
        "quantity": 11,
        "average_price": 1126.65
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock = request.form['stock']
        purchase_price = float(request.form['purchase_price'])
        quantity = int(request.form['quantity'])
        average_price = float(request.form['average_price'])  # Added average price input

        stocks[stock] = {
            "code": stock,
            "price": purchase_price,
            "quantity": quantity,
            "average_price": average_price
        }

    stock_data = []

    total_invested_amount = 0
    total_current_amount = 0

    codes = [details["code"] for details in stocks.values()]
    quotes = b.getScripCodesData(codes)

    for stock, details in stocks.items():
        code = details["code"]
        purchase_price = details["price"]
        quantity = details["quantity"]
        average_price = details["average_price"]

        quote = quotes[code]
        current_price = float(quote["currentValue"])

        if current_price > purchase_price:
            profit = int((current_price - purchase_price) * quantity * 1.5)
            color = "green"
            status = f"Profit: {profit}"
            action = "Wait"
            action_color = "red"
        elif current_price == purchase_price:
            color = "black"
            status = "No Profit No Loss"
            action = "Wait"
            action_color = "red"
        elif current_price > average_price:
            profit = int((current_price - purchase_price) * quantity * 1.5)
            color = "green"
            status = f"Profit: {profit}"
            action = "Sell"
            action_color = "green"
        else:
            loss = int((purchase_price - current_price) * quantity)
            color = "red"
            status = f"Loss: {loss}"
            action = "Wait"
            action_color = "red"

        invested_amount = purchase_price * quantity
        current_amount = current_price * quantity

        total_invested_amount += invested_amount
        total_current_amount += current_amount

        stock_data.append({
            "stock": stock,
            "purchase_price": purchase_price,
            "quantity": quantity,
            "current_price": current_price,
            "average_price": average_price,
            "status": status,
            "color": color,
            "action": action,
            "action_color": action_color,
            "invested_amount": invested_amount,
            "current_amount": current_amount
        })

    return render_template('stock_information.html', stocks=stock_data, total_invested_amount=total_invested_amount, total_current_amount=total_current_amount)

if __name__ == '__main__':
    app.run()
