#!/usr/bin/env python
import pika
import video_to_frames
import constant
import json
import os

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='simulations')
channel.queue_declare(queue='results')


def callback(ch, method, properties, body):
    requestParams = json.loads(body.decode('utf-8'))
    fileName = os.path.join(constant.ASSET_DIR, requestParams[0])
    print(fileName)
    results = video_to_frames.FrameCapture(fileName)

    # send a message back
    channel.basic_publish(exchange='', routing_key='results',
                          body=json.dumps(results, ensure_ascii=False))


# receive message and complete simulation
channel.basic_consume(callback, queue='simulations', no_ack=True)

channel.start_consuming()
