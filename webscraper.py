from bs4 import BeautifulSoup
import requests

def getCurrencyCodesAndInfo():
    """Retrieves currency codes and related info from a website"""
    response = requests.get("https://docs.1010data.com/1010dataReferenceManual/DataTypesAndFormats/currencyUnitCodes.html")
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find("tbody")

    tags = result.find_all("tr")

    countries = []
    currencies = []
    codes = []
    for tag in tags:
        temp = []
        for i in range(1, 4):
            key = f"topic_m4v_rt3_5r__table_k2t_fv3_5r__entry__{i}"
            entry = tag.find(headers=key)
            temp.append(entry.text)

        if temp[1] == " ":
            continue
        countries.append(temp[0])
        currencies.append(temp[1])
        codes.append(temp[2])

        if temp[2] == "ZWL":
            break

    return countries, currencies, codes


def find_exchange_amount(fromCurrency, toCurrency, amount):
    """Gets the exchange rate between """
    url = f"https://www.x-rates.com/calculator/?from={fromCurrency}&to={toCurrency}&amount={amount}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    tag = soup.find("span", class_="ccOutputRslt")

    return tag.text


