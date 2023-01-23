# Inventory & Payment API

Its a simple API to simulate microservices with python using FastAPI framework and use RedisJSON as a Database and dispatch events with Redis Streams. RedisJSON is a NoSQL database just like MongoDB and Redis Streams is an Event Bus just like RabbitMQ or Apache Kafka.


## Setup APIs

1. create python work env

        python3 -m venv {{env_name}}



2. Active env

        source ./{{env_name}}/bin/active

3. Install dependencies

4. Open 4 terminals every on has env is active

5. In first and second terminals run 

        cd ./inventory

6. In first terminal run 

        uvicorn main:app --reload

7. In second terminal run inventory consumer

        python3 consumer.py

8. In third and forth terminal run

        cd ./payments

9. In third terminal u need to run payment server and change port run 

        uvicorn main:app --reload --port=8001

10. In forth terminal run payment consumer

        python3 consumer.py

Now ur env is ready.


## API Document

After run server u can open ur browser and enter

    {{server}}/docs
