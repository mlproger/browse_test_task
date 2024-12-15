from pika import ConnectionParameters, BlockingConnection, PlainCredentials
from dotenv import load_dotenv
import json
import os
from selenium import webdriver
import logging
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logging.basicConfig(level=logging.INFO, filename="consumer_log.log",filemode="w")

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

def get_selenium_driver():

    selenium_hub_url = "http://selenium-hub:4444/wd/hub"  


    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")  

    return webdriver.Remote(command_executor=selenium_hub_url, options=options)




def process_message(channel, method, properties, body):
    body = json.loads(body.decode('utf-8'))
    url = body.get("url")
    if not url:
        logging.info(f"[Consumer] No url in task!")
    else:
        driver = None
        try:
            driver = get_selenium_driver()

        
            driver.get(url)
            html_content = driver.page_source
            logging.info(f"[Consumer] {html_content}")

            driver.quit()
            
        except Exception as e:
             logging.info(f"[Consumer] Bad url!")
        finally:
            try:
                driver.quit()
            except:
                pass

    channel.basic_ack(delivery_tag=method.delivery_tag)
    



def get_task():
    with BlockingConnection(params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue="test")
            ch.basic_consume(queue="test", on_message_callback=process_message)
            logging.info("[Consumer] WAIT...")
            ch.start_consuming()


if __name__ == "__main__":
    get_task()