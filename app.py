from flask import Flask, render_template, request
from bsedata.bse import BSE

app = Flask(__name__)

b = BSE()

# Stocks With Their Company Code
stocks = {
    "TATA_POWER": {
        "code": "500400",
        "price": 205,
        "quantity": 40
    },
    "TATA_MOTORS": {
        "code": "500570",
        "price": 524,
        "quantity": 15
    },
    "TATA_CONSULTANCY_SERVICES": {
        "code": "532540",
        "price": 3244,
        "quantity": 12
    },
    "Sona_BLW_Precision_Forgings": {
        "code": "543300",
        "price": 540,
        "quantity": 15
    },
    "HDFC_Bank": {
        "code": "500180",
        "price": 1648,
        "quantity": 19
    },
    "Aether_Industries": {
        "code": "543534",
        "price": 915,
        "quantity": 11
    },
    "Clean_Science_and_Technology": {
        "code": "543318",
        "price": 1495,
        "quantity": 6
    },
    "DYNEMIC_PRODUCTS": {
        "code": "532707",
        "price": 323,
        "quantity": 91
    },
    "Laxmi_Organic_Industries": {
        "code": "543277",
        "price": 275,
        "quantity": 75
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