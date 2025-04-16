FROM python

WORKDIR /fastapi
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app/utils/certs/gen_keys.py"]
CMD main.py