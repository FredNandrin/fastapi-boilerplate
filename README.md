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