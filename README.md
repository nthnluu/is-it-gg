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

```bash
data = [timestamp, currentGold, level, xp, minionsKilled, firstBlood, firstTower]
logistic_regression.predict((np.array(data).reshape(1, -1)))
```


## License
[MIT](https://choosealicense.com/licenses/mit/)