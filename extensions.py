import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество валюты {amount}.")

        if amount <= 0:
            raise APIException(f"Не возможно конверстировать количество валюты меньше или равно 0")


        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")

        exchange_course = json.loads(r.content)[keys[quote]]
        total_amount = float(amount)*float(exchange_course)
        return total_amount