from main import redis, Order
import time

key = 'refund_order'
group = 'payment-group'

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
                order = Order.get(order_obj['pk'])
                order.status = "refunded"
                order.save()
                print("process event done!")
    except Exception as e:
        print(str(e))

    time.sleep(1)