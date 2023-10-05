from asyncio.log import logger
from Stocker import stocks
from Catalog import catalog
logger = catalog.CataLog()
itc = stocks.Stock("ITC","ITC.NS")
response = itc.download()
logger.info(response.text)