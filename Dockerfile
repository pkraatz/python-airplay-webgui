FROM alpine:3.5

# Add virtual packes for build
RUN apk add --no-cache --virtual .build-deps python-dev build-base linux-headers

# Add needed packages for runtime and install python-airplay
RUN apk add --no-cache --update py2-pip \
    && pip install --upgrade pip \
    && pip install https://github.com/pkraatz/python-airplay/archive/transcode.zip

# install Python modules needed by the Web GUI app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Remove build dependencies
RUN apk del .build-deps

# copy files required for the app to run
COPY app.py /usr/src/app/
COPY templates/index.html /usr/src/app/templates/
COPY templates/layout.html /usr/src/app/templates/

EXPOSE 49913

# run the application
CMD ["python", "/usr/src/app/app.py"]
