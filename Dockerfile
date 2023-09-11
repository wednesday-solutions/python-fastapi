FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN  pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000"]
