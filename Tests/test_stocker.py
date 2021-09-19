from Stocker import stocks

def test_Stocker():
    itc = stocks.Stock("ITC", "ITC.NS")
    itc.clean()
    itc.config()
    tcs = stocks.Stock("TCS", "TCS.NS")
    tcs.clean()
    tcs.config()
    assert itc.dates == tcs.dates