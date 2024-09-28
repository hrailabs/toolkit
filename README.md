<h1><b>Instructions</b></h1>

<b>Installation:</b>
<li>Set up a virtual environment: `equity_toolkit`
<li>`conda env create -f env.yaml`
<li>`conda activate equity_tookit`

<b>File Prep:</b>
<li>Place input csv file in `inputs` folder.
<li>Update `config` file with parameters.

<b>Run App:</b>
<li>`python app.py`
<li>Navigate to local browser: http://127.0.0.1:8050/

<b>Run Model:</b>
```import yaml
import model

with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
model = model.Model(config)

df_prep, tbl = model.prep()

df_result = model.analysis(df_prep.copy(), tbl)
```

#to do, add legalese
#add api reference
#add use case
#add a notebooks file
