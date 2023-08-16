# build_MTV0.8
source code for build ManyTypes4Py Version 0.8

## build dataset
main script: build_dataset.py
collect & download & deduplicate the dataset
### install buildmt
```python
git clone https://github.com/LangFeng0912/build_MTV0.8.git
pip install -e build_MTV0.8/
```
### collect raw dataset
```python
buildmt build
```

## data process & Augmentation
requires Ubuntu version ubuntu 20 or newer, based on Libsa4Py
### build docker image
```
docker build -t libsa4py .
```

### run docker
```
docker run -it -v [source]:/data/source -v [result]:/data/results libsa4py 
```
> `[source]` refers the location for the raw dataset in the local machine, 
> for example: `raw_projects`
>
> `[result]` refers the location for the processed dataset in the local machine,
> for example: `processed_projects`


### install watchman manually
```python
dpkg -i watchman_ubuntu20.04_v2022.12.12.00.deb
apt-get -f -y install
watchman version
```

### run libsa4py with pyre options
```python
cd data
libsa4py process --p source --o results --pyre
```