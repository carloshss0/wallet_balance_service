import asyncio
import json
from aiokafka import AIOKafkaConsumer

from wallet_balance_service.db.models import Balance
from .db.db import SessionLocal

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "balances"

async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()

    try:
        async for msg in consumer:
            data = msg.value["Payload"]
            print(data)
            account_id_from = data["account_id_from"]
            balance_account_id_from = data["balance_account_id_from"]
            account_id_to = data["account_id_to"]
            balance_account_id_to = data["balance_account_id_to"]

            with SessionLocal() as db:
                balance_from = db.query(Balance).get(account_id_from)
                if not balance_from:
                    balance_from = Balance(account_id=account_id_from, balance=balance_account_id_from)
                    db.add(balance_from)
                else:
                    balance_from.balance_account_id_from = balance_account_id_from
                
                balance_to = db.query(Balance).get(account_id_to)
                if not balance_to:
                    balance_to = Balance(account_id=account_id_to, balance=balance_account_id_to)
                    db.add(balance_to)
                else:
                    balance_to.balance_account_id_to = balance_account_id_to

                db.commit()
    finally:
        await consumer.stop()

                
