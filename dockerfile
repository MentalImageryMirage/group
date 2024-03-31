FROM python
WORKDIR /groupchatbot
COPY . /groupchatbot

RUN pip install -r requirements.txt

CMD python chatbot.py