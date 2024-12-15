from pika import ConnectionParameters, BlockingConnection, PlainCredentials
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, filename="producer_log.log",filemode="w")


import json
import os
load_dotenv()



params = ConnectionParameters(
    host=os.environ.get("HOST"),
    port=os.environ.get("PORT"),
    credentials=PlainCredentials(os.environ.get("USER"), os.environ.get("PASSWORD"))
)

# params = ConnectionParameters(
#     host="localhost",
#     port=5672,
#     credentials=PlainCredentials("guest", "guest")
# )



def publish_task(task):
    with BlockingConnection(params) as conn:
        with conn.channel() as chanel:
            chanel.queue_declare(queue="test")
            chanel.basic_publish(exchange='', routing_key="test", body=json.dumps(task))
            logging.info("[Producer] Task published!")


# if __name__ == "__main__":
#     for i in range(5):
#         publish_task("hi")