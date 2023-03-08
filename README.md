# Flask App with Celery and Redis

This is an example Flask app that uses Celery as the job queue system and Redis as the caching mechanism to process NFT images using AI services. The app allows you to submit an NFT image for processing and check the status of the processing task.

## Getting Started

To run the app locally, follow these steps:

1. Clone the repository:
```
git clone https://github.com/W8gReZW/flask-celery-redis.git
cd flask-celery-redis
```

2. Install the dependencies:
```
pip install -r requirements.txt
```

3. Start a Redis instance:
```
docker run --name redis -d -p 6379:6379 redis
```
4. Start the Celery worker:
```
celery -A app.celery worker --loglevel=INFO
```

5. Start the Flask app:
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

6. Submit an NFT image for processing:
```
curl -X POST -H "Content-Type: application/json" -d '{"image_path": "path/to/image.png"}' http://localhost:5000/process_nft_image
```

7. Check the status of the processing task:
```
curl http://localhost:5000/task_status/<task_id>
```


## Deploying on Render.com

To deploy the app on Render.com, follow these steps:

1. Create a new web service and select "Python" as the language.

2. In the "Environment Variables" section, add the following variable:

- `REDIS_URL`: The Redis URL for the Celery broker and result backend. You can use the default Redis instance on Render (`redis://localhost:6379/0`) or a Redis instance from a Redis add-on.

3. In the "Advanced" section, add the following values:

- `Start Command`: `celery -A app.celery worker --loglevel=INFO`
- `Environment`: `python` (or select a custom environment with Python and Redis installed)

4. Click "Create Web Service" to deploy the app on Render.com.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.





