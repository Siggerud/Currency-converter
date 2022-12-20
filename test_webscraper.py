from webscraper import getCurrencyCodesAndInfo, find_exchange_amount


def test_getCurrencyCodesAndInfo():
    countries, currencies, codes = getCurrencyCodesAndInfo()

    assert currencies[0] == "Afghani"
    assert currencies[-1] == "Zimbabwe Dollar"
    assert countries[1] == "ÅLAND ISLANDS"
    assert countries[-1] == "ZIMBABWE"
    assert codes[2] == "ALL"
    assert codes[-1] == "ZWL"


def test_find_exchange_rate():
    assert 0.2 < float(find_exchange_amount("NOK", "USD", 5).split()[0]) < 0.7
    assert 1.5 < float(find_exchange_amount("USD", "EUR", 2).split()[0]) < 2.5
    assert 2.0 < float(find_exchange_amount("JPY", "CNY", 50).split()[0]) < 3









