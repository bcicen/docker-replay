# Run docker-replay inside Docker
# You must bind your Docker socket to the container
#
# Example:
# docker build -t replay .
# docker run -v /var/run/docker.sock:/var/run/docker.sock replay -p nginx

FROM python:3.4-alpine

WORKDIR /usr/src/app
COPY . .
RUN pip install .

ENTRYPOINT ["docker-replay"]