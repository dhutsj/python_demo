# start by pulling the python image
FROM python:3.7

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

# copy every content from the local file to the image
COPY . /app

EXPOSE 5000

RUN opentelemetry-bootstrap -a install

CMD opentelemetry-instrument --traces_exporter console --metrics_exporter console flask run
