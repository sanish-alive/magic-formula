from bs4 import BeautifulSoup
import requests
import re
import webScraping

def dataExtraction(companies):

    for symbol in companies.keys():
        
        company_data = webScraping.companyDataExtraction(symbol)
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
