FROM public.ecr.aws/lambda/python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY model/ ./model/

# CMD is for Lambda's ENTRYPOINT. It points to your app handler.
# If using Lambda Web Adapter, it typically runs the web server:
# CMD ["python", "-m", "awslambdaric", "app.app"]
# (Requires installing 'aws-lambda-rie' and 'lambda-web-adapter' in requirements.txt)
# Or, if not using web adapter, directly call your Flask app.
# This is complex due to the way Lambda expects handlers.
# Sticking with a Flask app and web adapter is easier.
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080" ]
# In a real setup, you'd integrate the Lambda Web Adapter
# FROM public.ecr.aws/lambda/python:3.9-arm64
# COPY requirements.txt ${LAMBDA_TASK_ROOT}
# RUN pip install -r requirements.txt
# COPY . ${LAMBDA_TASK_ROOT}
# CMD ["app.app"] # Assuming your Flask app instance is named 'app' in app.py
