# nearest_city_distance

Program to detect the distance to the nearest city based on the coordinates indicated when running the program.

**View Documentation:** [nearest_city_distance Documentation](https://awacero.github.io/nearest_city_distance/index.html)

## Clone nearest_city_distance code

``` bash
git clone https://github.com/awacero/nearest_city_distance.git

```

## Installation

``` bash
cd neanearest_city_distance/
conda env create -f environment.yml
conda activate nearest_city
```


## Run nearest_city_distance

``` bash
conda activate nearest_city
cd neanearest_city_distance/
python manage.py
```

**Go to URL:** http://127.0.0.1:5000/get_nearest_city?lat=-2.71&lon=-78.56&token=clavemuysecreta

## How to run test

``` bash
cd PATH_PROJECT
pytest
```

## Result

If the program execution is successful, it should be displayed:
1) Distance 
2) City
3) Province or State


