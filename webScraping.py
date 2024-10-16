from bs4 import BeautifulSoup
import time
import requests
import re

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


def openIPO():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    url = 'https://merolagani.com/Index.aspx'
    r = requests.get(url, headers=headers)

    print(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('table', class_='table table-striped table-hover table-zeromargin')

    rows = table.find_all('tr')[1:]  # Skip the header row

    data = []
    for row in rows:
        columns = row.find_all('td')
        status = columns[6].text.strip()
        if status == "Open":
            company = columns[0].find('a').text.strip()
            title = columns[0].find('a')['title'].strip()
            open_date = columns[3].text.strip()
            close_date = columns[4].text.strip()
            detail = columns[7].find('a')['title'].strip()
            

            data.append({
                'company': company,
                'title': title,
                'open_date': open_date,
                'close_date': close_date,
                'detail': detail
            })

    return data
    
if __name__ == '__main__':
    print(openIPO())