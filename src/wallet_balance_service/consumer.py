import asyncio
import json
from aiokafka import AIOKafkaConsumer
import os

from wallet_balance_service.db.models import Balance
from .db.db import SessionLocal

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
TOPIC_NAME = "balances"

async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    for _ in range(10):
        try:
            await consumer.start()
            break  # conseguiu conectar, sai do loop
        except:
            print("Kafka is not ready, trying again in 3s...")
            await asyncio.sleep(3)
    else:
        print("Was not able to connect with kafka after several attempts")
        return

    try:
        async for msg in consumer:
            data = msg.value["Payload"]
            print(data)
            account_id_from_data = data["account_id_from"]
            balance_from_data = data["balance_account_id_from"]
            account_id_to_data = data["account_id_to"]
            balance_to_data = data["balance_account_id_to"]

            with SessionLocal() as db:
                balance_from = db.query(Balance).get(account_id_from_data)
                if not balance_from:
                    balance_from = Balance(account_id=account_id_from_data, balance=balance_from_data)
                    db.add(balance_from)
                else:
                    balance_from.balance = balance_from_data
                
                balance_to = db.query(Balance).get(account_id_to_data)
                if not balance_to:
                    balance_to = Balance(account_id=account_id_to_data, balance=balance_to_data)
                    db.add(balance_to)
                else:
                    balance_to.balance = balance_to_data

                db.commit()
    finally:
        await consumer.stop()

                
