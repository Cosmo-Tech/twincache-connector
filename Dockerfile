FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY TwinCache_Connector/ TwinCache_Connector/
CMD python TwinCache_Connector/__init__.py