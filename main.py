import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

class ExchangeRateFetcher:
    def __init__(self):
        self.base_url = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch_exchange_rate(self, date):
        url = f"{self.base_url}{date}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = data["exchangeRate"]
                    filtered_rates = [{rate['currency']: rate['saleRateNB']} for rate in rates if rate['currency'] in ('USD', 'EUR')]
                    return filtered_rates
                else:
                    print(f"Error fetching data for {date}: {response.status}")

async def main(num_days):
    fetcher = ExchangeRateFetcher()
    dates = [datetime.strftime(datetime.now() - timedelta(days=i), "%d.%m.%Y") for i in range(1, num_days + 1)]
    tasks = []

    for date in dates:
        tasks.append(fetcher.fetch_exchange_rate(date))

    results = await asyncio.gather(*tasks)

    print("Exchange rates:")
    for date, rates in zip(dates, results):
        print(f"For {date}:")
        for rate in rates:
            print(rate)
        print()
    
if __name__ == "__main__":
    if sys.argv[1].isdigit():
        if 0<int(sys.argv[1])<10:
            number_of_days = int(sys.argv[1])
    else:
        print("Incorrect input, fetching last 10 days instead...")
        number_of_days = 10

    

    asyncio.run(main(number_of_days))
