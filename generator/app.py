# destination/main.py
import os
import json
import kafka_interface as kafka
import mongodb_interface as mongo

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TOPIC_OUTPUT = os.environ.get('TOPIC_OUTPUT')
DATABASE = os.environ.get('DATABASE')

if __name__ == '__main__':
    producer = kafka.connectProducer(server = KAFKA_BROKER_URL)
    db = mongo.get_db(DATABASE)
    collections = db.list_collection_names()
    for collectionName in collections:
        collection = db[collectionName]
        for document in collection.find():
            content = {
                'domain': document['domain'],
                'TaggedClusters': document['TaggedClusters']
            }
            content_json = json.dumps(content)
            kafka.send_message(producer=producer, topic=TOPIC_OUTPUT, value=content_json)

