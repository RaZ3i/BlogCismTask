FROM python:3.12 


RUN mkdir /fastapi_app


WORKDIR /fastapi_app


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY . .


# RUN chmod a+x docker/*.sh

WORKDIR /src

CMD uvicorn main:app --fd=0.0.0.0:8000