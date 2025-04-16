FROM python

WORKDIR /fastapi
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD /bin/bash -c "python app/utils/certs/gen_keys.py && python main.py"