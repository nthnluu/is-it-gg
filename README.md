# Is it GG?

A binary classification algorithm that determines whether you won or lost a League of Legends game given your current in-game stats.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage
Generate a dataset using the Riot API by adding your [development API key]('https://developer.riotgames.com/'):

```python
# collect_data.py
import requests
import json

riot_api_key = 'YOUR API KEY GOES HERE'
```
Launch Jupyter Notebook:

```bash
jupyter notebook
```
Make a prediction:

```python
predict(timestamp=1187000, currentGold=1340, level=10, minionsKilled=88, firstBlood=True, firstTower=True) # Won
predict(timestamp=1187000, currentGold=123, level=4, minionsKilled=12, firstBlood=False, firstTower=True) # Loss
```


## License
[MIT](https://choosealicense.com/licenses/mit/)