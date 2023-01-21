from main import redis, Product
import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis.xgroup_create(key, group)
except:
    print("already exist man!!!!")



while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        if results != []:
            for result in results:
                order_obj = result[1][0][1]
                try:
                    product = Product.get(order_obj['product_id'])
                    product.quantity = product.quantity - int(order_obj['quantity'])
                    product.save()
                    print("process event done!!")
                except:
                    redis.xadd('refund_order', order_obj, '*')
    except Exception as e:
        print(str(e))

    time.sleep(1)