# ASI_Grupa4

## Run tutorial:
* Create conda environment:
```
conda create --name kedro-environment python=3.10 -y
conda activate kedro-environment
conda install -c conda-forge kedro
conda install -c conda-forge kedro-viz
conda activate kedro-environment
```
* Install kedro dependencies:
```
cd kedro-asi/
pip install -r src/requirements.txt
```
* Run first kedro pipeline separately:
```
kedro run --pipeline data_loading
```
If it works, now you are free to use pipeline :)