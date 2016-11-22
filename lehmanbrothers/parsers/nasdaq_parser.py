@staticmethod
def fetch_statement(symbol, query='income-statement'):
    r = requests.get(
        'http://www.nasdaq.com/symbol/{symbol}/financials?query={query}'.format(
            symbol=symbol, query=query))
    soup = BeautifulSoup(r.content, 'html.parser')
    div = soup.find('div', attrs={'class': 'genTable'})
    table = div.find('table')
    rows = table.find_all('tr')
    statements = []
    result = []
    for row in rows:
        header = row.find('th')
        if header:
            header = header.text.lower().replace(' ', '_').replace(':',
                                                                   '').replace(
                "'", "").replace('/',
                                 '-').replace(
                '.', '').replace(',', '')
            cols = row.find_all('td')
            if header == 'period_ending':
                cols = row.find_all('th')
            cols = [ele.text.strip().split('/')[-1] for ele in cols if ele]
            # cols.insert(0, header)
            attribute = [header] + cols[-4:]
            statements.append(attribute)

    # print(len(cols[-4:]))
    for i in range(1, len(cols[-4:])):
        # print(i+1)
        yearly = {item[0]: item[i] for item in statements if len(item) > 1}
        result.append(yearly)
    return result

