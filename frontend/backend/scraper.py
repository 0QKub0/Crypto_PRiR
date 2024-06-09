import asyncio
import aiohttp
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi

databaseURL = 'mongodb+srv://desirecutieqb:Bloodqkub36@baza1.kxccyjn.mongodb.net/?retryWrites=true&w=majority&appName=Baza1'
client = MongoClient(databaseURL, server_api=ServerApi('1'))
db = client.crypto_db
collection = db.crypto_collection
alerts_collection = db.alerts

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def scrape_prices():
    urls = {
        'BTC': 'https://coinmarketcap.com/currencies/bitcoin/',
        'ETH': 'https://coinmarketcap.com/currencies/ethereum/',
        'TON': 'https://coinmarketcap.com/currencies/toncoin/'
    }
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls.values()]
        responses = await asyncio.gather(*tasks)

    data = []
    for (crypto, response) in zip(urls.keys(), responses):
        soup = BeautifulSoup(response, 'html.parser')
        price = soup.find('span', class_='sc-d1ede7e3-0 fsQm base-text').text if soup.find('span', class_='sc-d1ede7e3-0 fsQm base-text') else 'N/A'
        volume = soup.find('dd', class_='sc-d1ede7e3-0 hPHvUM base-text').text if soup.find('dd', class_='sc-d1ede7e3-0 hPHvUM base-text') else 'N/A'
        percent_change = soup.find('p', class_='sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI').text if soup.find('p', class_='sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI') else 'N/A'
        market_cap = soup.find('dd', class_='sc-d1ede7e3-0 hPHvUM base-text').text if soup.find('dd', class_='sc-d1ede7e3-0 hPHvUM base-text') else 'N/A'

        price_float = float(price.replace('$', '').replace(',', ''))
        alerts = alerts_collection.find({'crypto': crypto})
        for alert in alerts:
            if price_float >= alert['price_threshold']:
                print(f"Uwaga: {crypto} price has reached ${price_float} which is above the threshold ${alert['price_threshold']}")
                alerts_collection.delete_one(alert)

        data.append({
            'crypto': crypto,
            'price': price,
            'volume': volume[5:],
            'percent_change': percent_change,
            'market_cap': market_cap[5:]
        })

    collection.delete_many({})
    collection.insert_many(data)

async def main():
    while True:
        await scrape_prices()
        await asyncio.sleep(60)

def scrape():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

if __name__ == '__main__':
    scrape()