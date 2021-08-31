FROM python:3.7

COPY ./apps /apps
WORKDIR /apps
RUN set -ex && \
    pip install -r requirements.txt 
EXPOSE 8040
CMD ["python", "index.py"]