# docker-replay
Generate `docker run` command and options from running containers

## Installing

```bash
pip install docker-replay
```

## Usage

```bash
docker-replay -p <container name or id>
```

output:
```bash
docker run --env PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
           --hostname test \
           --interactive \
           --tty \
           --add-host google.com:127.0.0.1 \
           --memory 128m \
           --memory-swap 256m \
           --memory-swappiness -1 \
           --name test \
           --expose 80/tcp \
           --restart on-failure:0 \
           --entrypoint "echo" \
           alpine:latest \
           hello
```

## Options

Option | Description
--- | ---
--debug, -d | enable debug output
--pretty-print, -p | pretty-print output
