<h1><b>Instructions</b></h1>

Place input csv file in `inputs` folder.
<br>Update `config` file with parameters.

<b>Run App:</b>
<br>`python app.py`
<br>Navigate to local browser: http://127.0.0.1:8050/

<b>Run Model:</b>
```import yaml
import model

with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
model = model.Model(config)

df_prep, tbl = model.prep()

df_result = model.analysis(df_prep.copy(), tbl)

# to do, add legalese
# add api reference
# add use case
# add a notebooks file
