# docker-replay
Generate `docker run` command and options from running containers

## Installing

```bash
pip install docker-replay
```

### Usage

```bash
docker-replay -p <container name or id>
```

output:
```bash
docker run --entrypoint="/bin/sh" \
           --interactive \
           --name=high_fermat \
           --tty \
           --user=nobody \
           --volume=/tmp/test:/target:ro
```
