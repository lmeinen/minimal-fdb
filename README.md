# FDB Server — Local Testing Setup

## Prerequisites

- Podman 4.x
- `podman-compose` installed (`pip install podman-compose`)
- `eccodes_definitions.edzw-2.44.0-1.tar.bz2` present in the working directory

## Build context

```
.
├── Dockerfile.fdb-server
├── Dockerfile.fdb-archive
├── docker-compose.yml
├── archive-file.py
├── requirements.txt
├── definitions.edzw-2.44.0-1.tar.bz2
└── config/
    ├── schema
    ├── catalogue/
    │   └── config.yaml
    ├── store_1/
    │   └── config.yaml
    └── client/
        └── config.yaml
```

## Build

Build the server image:

```sh
podman build -f Dockerfile.fdb-server -t fdb-server:5.19 .
```

Build the archive client image:

```sh
podman build -f Dockerfile.fdb-archive -t fdb-archive:5.19 .
```

## Start the FDB server

```sh
podman compose up --detach
```

Check that catalogue and store are running:

```sh
podman compose ps
podman compose logs --follow
```

## Archive a GRIB file

Place your GRIB file in a local `data/` directory, then run:

```sh
podman run --rm \
  --network minimal-fdb_fdb \
  -v ./config/client/config.yaml:/etc/fdb/config.yaml:ro \
  -v ./data:/data:ro \
  fdb-archive:5.19 /data/lfff00000000c
```

## Inspect FDB contents

```sh
podman run --rm \
  --network minimal-fdb_fdb \
  -v ./config/client/config.yaml:/etc/fdb/config.yaml:ro \
  --entrypoint fdb-list
  fdb-archive:5.19 date=20260407,time=0600,model=icon-ch1-eps,class=od,expver=0001,stream=enfo
```

## Stop the FDB server

```sh
podman compose down
```

To also remove the FDB root volume (all archived data will be lost):

```sh
podman compose down --volumes
```

## Clean up all Podman state

```sh
podman system prune --all --volumes
```
