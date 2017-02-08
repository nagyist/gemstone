import json

import pika

from gemstone.event.transport.base import BaseEventTransport


class RabbitMqEventTransport(BaseEventTransport):
    EXCHANGE_PREFIX = "gemstone.events."

    def __init__(self, host="127.0.0.1", port=5672, username="", password="", **connection_options):
        self._handlers = {}

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host, port=port, credentials=pika.PlainCredentials(username=username, password=password),
                **connection_options
            )
        )
        self.channel = self.connection.channel()

    def register_event_handler(self, handler_func, handled_event_name):
        self._handlers[handled_event_name] = handler_func

    def start_accepting_events(self):
        for event_name, event_handler in self._handlers.items():
            current_exchange_name = self.EXCHANGE_PREFIX + event_name
            self.channel.exchange_declare(
                exchange=current_exchange_name,
                type="fanout"
            )
            result = self.channel.queue_declare(exclusive=True)
            queue_name = result.method.queue

            self.channel.queue_bind(exchange=current_exchange_name, queue=queue_name)

            self.channel.basic_consume(self._callback, queue=queue_name, no_ack=True)

        self.channel.start_consuming()

    def _callback(self, channel, method, properties, body):
        if not method.exchange.startswith(self.EXCHANGE_PREFIX):
            return

        event_name = method.exchange[len(self.EXCHANGE_PREFIX):]
        self.on_event_received(event_name, body)

    def on_event_received(self, event_name, event_body):
        handler = self._handlers.get(event_name)
        if not handler:
            return
        if isinstance(event_body, bytes):
            event_body = event_body.decode()

        handler(json.loads(event_body))

    def emit_event(self, event_name, event_body):
        self.channel.basic_publish(
            exchange=self.EXCHANGE_PREFIX + event_name,
            routing_key='',
            body=json.dumps(event_body)
        )

    def __del__(self):
        self.connection.close()


if __name__ == '__main__':
    def handler1(body):
        print("[!] {}".format(body))


    def handler2(body):
        print("QWQWEQQW {}".format(body))


    transport = RabbitMqEventTransport(host="192.168.1.71",
                                       credentials=pika.PlainCredentials(username="admin", password="X5f6rPmx1yYz"))

    transport.register_event_handler(handler1, "event_one")
    transport.register_event_handler(handler2, "event_two")

    transport.start_accepting_events()