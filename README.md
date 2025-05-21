# CI/CD instruction

## Project structure

### Check example before start [test](https://github.com/GoatsTEAM/backend/tree/main/test)

### You only need to edit - "<service_name>"

```
backend
    .github/workflows
    <service_name>
        ...
        apps
        ...
        Dokerfile -- must be
        deploy.yaml -- must be
        ...
    README.md
    test -- example
    test_2 -- example
    docker-compose.yaml
```

### Add it to main.py 

```
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(root_path="/<service_name>", title="<service_name>")

Instrumentator().instrument(app).expose(app)
```
### Create deploy.yaml at backend/<service_name>
```
service: <service_name>
compose: /home/deploy/backend
```


### Add it to docker-compose.yaml "like [test_2](https://github.com/GoatsTEAM/backend/blob/main/docker-compose.yaml)"

```
  <service_name>:
    build: ./<service_name>
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.<service_name>.rule=PathPrefix(`/<service_name>`)"
      - "traefik.http.routers.<service_name>.entrypoints=web"
      - "traefik.http.services.<service_name>.loadbalancer.server.port=80"
      - "traefik.http.middlewares.<service_name>-strip.stripprefix.prefixes=/<service_name>"
      - "traefik.http.routers.<service_name>.middlewares=<service_name>-strip"
    networks: [proxy]
```
### A litter more
- push to you branche 
- create pull request to main
- check pipline in [Actions](https://github.com/GoatsTEAM/backend/actions)
- after succession code, go to http://45.132.255.35/<service_name>/docs
---
### And one more thing, the service is deployed only when it finds changes with the previous commit, so if you have nothing to add, then delete or add an empty line
---
### If you have some problems, just ask Pavel
