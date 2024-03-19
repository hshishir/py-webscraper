# python webscraper

- This project scrapes through given list of website(s) recursively using selenium wire.  
- It identifies all downstream network calls that are API calls and downloads responses as JSON payloads to be used for ML training purposes

### Usage
#### Run locally
```
- Clone repo
- Run below commands
    > poetry install
    > poetry run pytest
    > poetry run py_webscraper parseurl 
    > poetry run python -m src.py_webscraper.cli
```

#### Run using docker

```
> docker build -f Dockerfile -t pywebscraper:0.1 .
> docker run --name pywebscraperct -it pywebscraper:0.1
```