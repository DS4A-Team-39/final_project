# Vulnex (Vulnerability Exploration)
## _Bucaramanga mayoralty_

#### Here you can find the applicaion working: [Vulnex App](https://vulnex.dployme.com/).

The mayoralty needs to locate and quantify the number of children and teens vulnerables in the 17 neighborhoods and 3 rural main areas of Bucaramanga and their relationship. In this application we use different tools to visualize trend changes in vulnerability between 2018 and 2020 for the following age groups: 
 - Early Childhood (0 to 5 years old)
 - Childhood(6 to 11 years old)
 - Adolescence (12 to 17 years old)

## Main Libraries
Based in Python 3.8 implementation
- Pandas
- Dash
- Flask
- psycopg2
- Numpy
- Plotly
- scikit-learn

## Integrations

 - PostgreSQL Database

## Architecture
<img src="https://github.com/DS4A-Team-39/final_project/blob/feature/esteban/apps/assets/img/architecture.png">

## Installation

Install the dependencies from requirements file

```sh
pip install -r requitements.txt
```
Run application
```sh
python apps/index.py
```

## Docker

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image

```sh
docker rmi -f dash
docker build -t dash .
docker run -p 8050:8050 dash
```

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8050 of the Docker (or whatever port was exposed in the Dockerfile):

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
localhost:8050
```

## License

**Free Software**


