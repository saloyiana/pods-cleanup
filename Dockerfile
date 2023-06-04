FROM python:3.8
 
WORKDIR /app
COPY . /app
 
RUN pip install -r requirements.txt
 
CMD ["python3", "failed_pod_clean_up.py"]