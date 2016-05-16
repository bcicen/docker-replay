# docker-rerun
Generate `docker run` command and options from running containers

## Installing

```bash
git clone https://github.com/bcicen/docker-rerun.git
cd docker-rerun
python setup install
```

### Usage

```bash
docker-rerun <container name or id>
```

output:
```bash
docker run --entrypoint="/bin/sh" --interactive --name=high_fermat --tty --user=nobody --volume=/tmp/test:/target:ro
```
