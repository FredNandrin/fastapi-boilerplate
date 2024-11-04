Init env

```
python3 -m venv venv
source venv/bin/activate

(venv)$ export PYTHONPATH=$PWD
```

Install required libraries

```
pip install -r requirements.txt
```

Run server

```
python main.py
```

Build and run docker instance

```
docker compose up --build
```

Run tests :

```
pytest
# or
ptw
```


# On Kubectl : 

```
kubectl apply -f mongo.yaml,mongo-express.yaml,server.yaml
minikube service python-api
minikube service mongo-express


```
# Locally
Launchh all services with docker :
```
docker compose up --build -d
```

When developping :
```
docker compose down server
python main.py
```
