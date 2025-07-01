from woocommerce import API
import json

wcapi = API(
    url="http://127.0.0.1:8888/localdemostore",
    consumer_key="your key here",
    consumer_secret="your secret here",
    version="wc/v3",
    timeout=15
)

# rs = wcapi.get("products")

payload = {"per_page": 90}
rs = wcapi.get("coupons", params=payload)
body = rs.json()
breakpoint()