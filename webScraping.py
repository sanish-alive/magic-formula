from bs4 import BeautifulSoup
import time
import requests
import re

def openIPO():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    url = 'https://merolagani.com/Index.aspx'
    r = requests.get(url, headers=headers)

    print(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('table', class_='table table-striped table-hover table-zeromargin')

    # Extracting header titles from the table
    headers = [header.get_text() for header in table.find_all('th')]

    # Create a list to store the rows
    table_data = []

    # Loop through each table row
    for row in table.find_all('tr')[1:]:  # [1:] to skip the header
        row_data = []
        
        # Loop through each cell in the row
        for cell in row.find_all('td'):
            row_data.append(cell.get_text(strip=True))  # strip=True will remove any leading/trailing spaces
        
        # Append the row data to the table data
        table_data.append(row_data)
        

    # Printing the extracted data
    # print(headers)
    output_table = []
    for row in table_data:
        if row[-2].lower() == 'open':
            output_table.append(row[0])
    return output_table


def PERatio(symbol):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    url = 'https://merolagani.com/CompanyDetail.aspx?symbol='+symbol.lower()
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')

    company_name = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_CompanyDetail1_companyName'}).text.strip()
    table = soup.find('table', {'id': 'accordion'})

    data = {}
    data['Company Name'] = company_name
    headers_to_extract = ["Market Price", "P/E Ratio", "EPS", "Book Value", "PBV"]

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


if __name__ == '__main__':
    # print(openIPO())
    print(PERatio('nifra'))
    # testing()