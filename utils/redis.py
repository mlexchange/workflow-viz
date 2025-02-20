import json
import os

import redis as redis


class RedisConn:
    def __init__(self, redis_conn: redis.Redis):
        self.redis_conn = redis_conn

    def get(self, key: str):
        return self.redis_conn.get(key)

    def set(self, key: str, value):
        self.redis_conn.set(key, value)

    def get_json(self, key: str):
        value_s = self.redis_conn.get(key)
        if value_s:
            values_js = json.loads(value_s)
        else:
            values_js = {}
        return values_js

    def set_json(self, key: str, value: dict):
        value_s = json.dumps(value)
        self.reddis_conn.set(key, value_s)

    def redis_subscribe(self, channel_name: str, callback: callable) -> None:
        """Listens for messages on a Redis Pub/Sub channel asynchronously."""
        pubsub = self.redis_conn.pubsub()
        channel_name = "scattering"
        pubsub.subscribe(channel_name)  # Subscribe to the channel

        print(f"Listening for messages on '{channel_name}'...")

        for message in pubsub.listen():
            if (
                message["type"] == "message"
            ):  # Ignore subscription confirmation messages
                if message["channel"] == channel_name:
                    callback(message["data"])

    @classmethod
    def from_settings(cls, settings: dict) -> "RedisConn":
        pool = redis.ConnectionPool(
            host=settings.host, port=settings.port, decode_responses=True
        )
        redis_conn = redis.Redis(connection_pool=pool)
        return cls(redis_conn)

    @classmethod
    def from_env(cls) -> "RedisConn":
        pool = redis.ConnectionPool(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=os.getenv("REDIS_PORT", 6379),
            decode_responses=True,
        )
        redis_conn = redis.Redis(connection_pool=pool)
        return cls(redis_conn)
