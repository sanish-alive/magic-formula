from flask import Flask, jsonify, request, render_template
import webScraping
import MagicFormula

app = Flask(__name__)

route = {
    'open-ipo': '/open-ipo',
    'magic-formula': '/magicformula'
}

@app.errorhandler(404)
def notFound(e):
    return "<center><h1>404<br>Page Not Found</h1></center>"

@app.route("/")
def helloFriend():
    return jsonify({'hello': 'friend'})

@app.route(route['open-ipo'])
def openIpo():
    return jsonify({'ipo': list(webScraping.openIPO())})

@app.route(route['magic-formula'], methods=['GET', 'POST'])
def magicFormulaForm():
    if request.method == 'POST':
        companies = {}
        # Iterate over form keys
        for key in request.form.keys():
            if key.endswith('_symbol'):
                # Extract the company name from the key
                selected_company = key.replace('_symbol', '')

                # Process the data for the selected company
                net_income = request.form.get(f'{selected_company}_netincome')
                total_asset = request.form.get(f'{selected_company}_totalasset')

                companies[selected_company] = {
                    "netIncome": float(net_income),
                    "totalAsset": float(total_asset)
                }
        print(companies)
        data = MagicFormula.dataExtraction(companies)
        return render_template("magictable.html", data=data)
    elif request.method == 'GET':
        return render_template("magicform.html")
    
    else:
        return "<center><h1>Request Method Wrong</h1></center>"

if __name__ == '__main__':
    app.run(debug=True)