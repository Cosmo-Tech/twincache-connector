FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY auth/ auth/
COPY TwinCache_Connector/ TwinCache_Connector/
COPY main.py main.py
CMD python main.py
