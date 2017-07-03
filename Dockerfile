# Run docker-replay inside Docker
#
# Example:
# docker build -t replay .
# docker run -v /var/run/docker.sock:/var/run/docker.sock replay -p nginx

FROM quay.io/vektorcloud/python:3

WORKDIR /usr/src/app
COPY . .
RUN pip install .

ENTRYPOINT ["docker-replay"]
