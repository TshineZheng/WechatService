FROM python:3.7.4-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 6637

CMD [ "python", "./wechat.py" ]
