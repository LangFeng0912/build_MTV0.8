# build_MTV0.8
source code for build ManyTypes4Py Version 0.8

## build dataset
main script: build_dataset.py
collect & download & deduplicate the dataset
### install buildmt
```python
git clone https://github.com/LangFeng0912/build_MTV0.8.git
pip install -r build_MTV0.8/requirements.txt
pip install build_MTV0.8/
```
### collect raw dataset
```python
buildmt build --p raw_projects --l 200 --j 4
```
> `[--p]` refers the location to collect the raw dataset : `raw_projects`
> 
> `[--l]` refers the numbers of project you want to collect
> 
>  `[--j]` refers the numbers of multi-processors
> 
> `[--c]` Whether to collect repos from Github [Optional, default=False]

### split raw dataset
```python
buildmt split --p raw_projects 
```
> `[--p]` refers the location to collect the raw dataset : `raw_projects`
> 
> 

# Docker Image
requires Ubuntu version ubuntu 20 or newer, based on Libsa4Py
### build docker image
```
docker build -t libsa4py .
```

### run docker
```
docker run -v [result]:/results libsa4py -l 32 -j 8
```
> `[source]` refers the location for the raw dataset in the local machine, 
> for example: `raw_projects`
>
> `[result]` refers the location for the processed dataset in the local machine,
> for example: `processed_projects`
> 
> `[--l]` refers the number of projects to download
> 
> `[--j]` refers the number of processors to use parallel


[//]: # (### install watchman manually)

[//]: # (```python)

[//]: # (dpkg -i watchman_ubuntu20.04_v2022.12.12.00.deb)

[//]: # (apt-get -f -y install)

[//]: # (watchman version)

[//]: # (```)

[//]: # (### activate vitrual environment)

[//]: # (```python)

[//]: # (source py38/bin/activate)

[//]: # (```)

[//]: # (### collect raw projects)

[//]: # (```python)

[//]: # (buildmt build --p raw_projects --l 200)

[//]: # (```)

[//]: # ()
[//]: # (### run libsa4py with pyre options)

[//]: # (```python)

[//]: # (libsa4py process --p raw_projects --o results --pyre --j 4)

[//]: # (```)