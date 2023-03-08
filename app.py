from flask import Flask, jsonify, request
from flask_cors import CORS
from celery import Celery
from redis import Redis
import os

app = Flask(__name__)
CORS(app)

# Configure Celery
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.config['CELERY_BROKER_URL'] = redis_url
app.config['CELERY_RESULT_BACKEND'] = redis_url
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Configure Redis
redis = Redis.from_url(redis_url)

# Define a task to process the NFT image
@celery.task(bind=True, max_retries=3, default_retry_delay=1)
def process_nft_image(self, image_path):
    # Check the cache first
    cache_key = 'image:' + image_path
    result = redis.get(cache_key)
    if result:
        return result.decode('utf-8')

    # Process the image using the AI services
    try:
        # TODO: Call the AI services and process the image
        result = {'success': True, 'message': 'Image processed successfully'}
        redis.set(cache_key, jsonify(result))
        return jsonify(result)
    except Exception as e:
        self.retry(exc=e)

# Define a route to submit the NFT image for processing
@app.route('/process_nft_image', methods=['POST'])
def submit_nft_image():
    image_path = request.json.get('image_path')
    task = process_nft_image.apply_async(args=[image_path])
    return jsonify({'task_id': task.id})

# Define a route to check the status of a task
@app.route('/task_status/<task_id>')
def check_task_status(task_id):
    task = process_nft_image.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'message': 'Task has not started yet'}
    elif task.state != 'FAILURE':
        response = {'state': task.state}
        if task.result:
            response['result'] = task.result
    else:
        response = {'state': task.state, 'message': str(task.info)}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
