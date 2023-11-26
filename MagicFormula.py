from bs4 import BeautifulSoup
import requests
import re

stock = {
    "nifra": {
        "netIncome": 234234234234,
        "Company Name": "Nepal Infrastructure Bank Limited (NIFRA)",
        "Sector": "Investment",
        "Shares Outstanding": 216_000_000,
        "Market Price": 187.00,
        "EPS": "7.66 (FY:080-081, Q:1)",
        "P/E Ratio": 24.41,
        "Book Value": 112.02,
        "PBV": 1.67,
        "Asset": 57868768
    },
    "nabil": {
        "netIncome": 234234,
        "Company Name": "Nabil Bank Limited (NABIL)",
        "Sector": "Commercial Banks",
        "Shares Outstanding": 270_569_970.00,
        "Market Price": 14.00,
        "EPS": "21.72 (FY:080-081, Q:1)",
        "P/E Ratio": 23.66,
        "Book Value": 218.27,
        "PBV": 2.35,
        "Asset": 87686546
    },
    "pli": {
        "netIncome": 3424,
        "Company Name": "Prabhu Life Insurance Limited (PLI)",
        "Sector": "Life Insurance",
        "Shares Outstanding": 21_960_000.00,
        "Market Price": 587.00,
        "EPS": "0.00 (FY:079-080, Q:3)",
        "P/E Ratio": 0.00,
        "Book Value": "127.20",
        "PBV": 4.61,
        "Asset": 79870989
    },
    "nica": {
        "netIncome": 234324,
        "Company Name": "NIC Asia Bank Ltd. (NICA)",
        "Sector": "Commercial Banks",
        "Shares Outstanding": 149_175_669.20,
        "Market Price": 503.00,
        "EPS": "27.09 (FY:080-081, Q:1)",
        "P/E Ratio": 18.57,
        "Book Value": 202.05,
        "PBV": "2.49",
        "Asset": 6576576765
    },
}

def companyDataExtraction(symbol):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    url = 'https://merolagani.com/CompanyDetail.aspx?symbol='+symbol.lower()
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')

    company_name = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_CompanyDetail1_companyName'}).text.strip()
    data = {}
    data['Company Name'] = company_name
    headers_to_extract = ["Market Price", "P/E Ratio", "EPS", "Book Value", "PBV", "Shares Outstanding", "Sector"]

    table = soup.find('table', {'id': 'accordion'})
    
    rows = table.find_all('tr')

    for row in rows:
        th = row.find('th')
        td = row.find('td')
        if th and td:
            header_text = th.text.strip()
            value = td.text.strip()
            value = re.sub(r'\s+', ' ', value).strip()
            if header_text in headers_to_extract:
                data[header_text] = value
    
    return data

def dataExtraction(companies):

    for symbol in companies.keys():
        
        company_data = companyDataExtraction(symbol)
        companies[symbol].update(company_data)

    return magicFormula(companies)


def magicFormula(companies):
    magic = {}
    for symbol in companies.keys():
        print(symbol)
        print(companies[symbol]["Shares Outstanding"])
        earningsPerShares = companies[symbol]["netIncome"] / float(companies[symbol]["Shares Outstanding"].replace(',', ''))
        print(f"EPS : {earningsPerShares}")
        PERatio = float(companies[symbol]["Market Price"].replace(',', '')) / earningsPerShares
        print(f"P/E: {PERatio}")

        returnOnAsset = companies[symbol]["netIncome"] / companies[symbol]["totalAsset"]
        print(f"ROA: {returnOnAsset}")

        magic[symbol] = {
            "companyName": companies[symbol]["Company Name"],
            "sector": companies[symbol]["Sector"],
            "marketPrice": float(companies[symbol]["Market Price"]),
            "bookValue": float(companies[symbol]["Book Value"]),
            "PBV": float(companies[symbol]["PBV"]),
            "EPS": round(earningsPerShares, 2),
            "P/E Ratio": round(PERatio, 2),
            "ROA": round(returnOnAsset, 2)
        }

    sortedPERatio = sorted(magic.items(), key=lambda x: x[1]["P/E Ratio"])

    # Assign P/E Ratio Rank
    for i, (symbol, company) in enumerate(sortedPERatio, start=1):
        company["P/E Ratio Rank"] = i

    # Sort the magic dictionary by ROA in descending order
    sortedROA = sorted(magic.items(), key=lambda x: x[1]["ROA"], reverse=True)

    # Assign ROA Rank
    for i, (symbol, company) in enumerate(sortedROA, start=1):
        company["ROA Rank"] = i

    # Print the results
    for symbol, company in magic.items():
        print(f"Symbol: {symbol}, P/E Ratio Rank: {company.get('P/E Ratio Rank')}::{magic[symbol]["P/E Ratio"]}, ROA Rank: {company.get('ROA Rank')}::{magic[symbol]["ROA"]}")
        magic[symbol].update({"Magic Formula Rank": company.get('P/E Ratio Rank')+company.get('ROA Rank')})

    return magic

if __name__ == '__main__':
    # magicFormula()
    # print(companyDataExtraction("nabil"))
    data = {'nifra': {'netIncome': 1.0, 'totalAsset': 2.0}, 'nabil': {'netIncome': 3.0, 'totalAsset': 4.0}, 'pli': {'netIncome': 5.0, 'totalAsset': 6.0}}

    dataExtraction(data)
