FROM python:3.8

COPY ./apps /apps
WORKDIR /apps
RUN set -ex && \
    pip install -r requirements.txt 
EXPOSE 8050
CMD ["python", "index.py"]