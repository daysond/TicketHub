import stripe
from decimal import *
stripe.api_key = "sk_test_Gaah29dliX1UUMIe3a6OAqqO00OQIP9EWO"

def create_prod(name, price,descrption):
    try:
        price_data = {"unit_amount": price, "currency":"cad"}
        
        res = stripe.Product.create(name=name, default_price_data=price_data)
        id = res["id"]
        price_id = res ["default_price"]
        print(f"id: {id} price id: {price_id}")
        print(res)
        return res
    except Exception as e:
        print(f"Failed uploading product. Error: {e}")
        raise e
