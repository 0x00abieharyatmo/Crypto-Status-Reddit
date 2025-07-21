import os
import praw
import requests
from datetime import datetime, timezone

def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "Bitcoin": data.get("bitcoin", {}).get("usd", "N/A"),
            "Ethereum": data.get("ethereum", {}).get("usd", "N/A"),
            "Solana": data.get("solana", {}).get("usd", "N/A"),
        }
    return {}

crypto = get_crypto_data()
today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

title = f"Crypto Market Update {today}"
body = (
    f"**Harga Cryptocurrency Hari Ini:**\n\n"
    f"- Bitcoin (BTC): ${crypto.get('Bitcoin')}\n"
    f"- Ethereum (ETH): ${crypto.get('Ethereum')}\n"
    f"- Solana (SOL): ${crypto.get('Solana')}\n\n"
    "Sumber data: [CoinGecko](https://coingecko.com)\n\n"
    "_Status ini dibuat otomatis setiap hari._"
)

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    username=os.environ['REDDIT_USERNAME'],
    password=os.environ['REDDIT_PASSWORD'],
    user_agent=os.environ['REDDIT_USER_AGENT']
)

subreddit = reddit.subreddit("VerticalCommunityID")  # Ganti dengan subreddit tujuan Anda
subreddit.submit(title, selftext=body)
