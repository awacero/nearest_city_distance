# nearest_city_distance

Program to detect the distance to the nearest city based on the coordinates indicated when running the program.

**View Documentation:** [nearest_city_distance Documentation](https://awacero.github.io/nearest_city_distance/index.html)

## Clone nearest_city_distance code:

``` bash
git clone https://github.com/awacero/nearest_city_distance.git

```

## Installation:

``` bash
cd nearest_city_distance/
conda env create -f environment.yml
conda activate nearest_city
```


## Run nearest_city_distance:

``` bash
conda activate nearest_city
cd nearest_city_distance/
python manage.py
```

**Go to URL:** http://127.0.0.1:5000/get_nearest_city?lat=-2.71&lon=-78.56&token=clavemuysecreta  

## Result:

If the program execution is successful, it should be displayed:
1) Distance 
2) City
3) Province or State  

![Screenshot from 2022-10-14 10-16-18](https://user-images.githubusercontent.com/102699851/195883498-e78d1bb8-a375-411c-b24a-b36ee1f0bef5.png)

## How to run test:

``` bash
cd PATH_PROJECT
pytest
```





