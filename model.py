from typing import Any
from pandas import DataFrame
from typing import Dict
from typing import List
from typing import Tuple

import yaml

import src.model_classes as mc 

with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
class Model:
    
    """
    
    """
    
    def __init__(
        self,
        config: Dict[str, Any]
    ):
        
        """
        
        """
        
        self.config = config

    def prep(
        self
    ) -> Tuple[DataFrame, List[float]]:
               
        """
        
        """
        
        config = self.config
        
        # ingest
        prep = mc.Ingest(config)
        df_prep: DataFrame = prep.run()

        # transform
        trans = mc.Transform(df=df_prep)
        tbl: List[float] = trans.run_build_cont_table()
        
        return df_prep, tbl
    
    def analysis(
        self,
        df_prep: DataFrame,
        tbl: List[float]
    ) -> DataFrame:
                     
        """

        """
        
        config = self.config

        stats = mc.StatsTesting2x2Cont(
            config=config,
            tbl=tbl,
            df=df_prep
        )
        df_result: DataFrame = stats.run_testing()
        
        return df_result
    
    
if __name__ == "__main__":
    
    model = Model()
    
    df_prep, tbl = model.prep()
    
    df_result = model.analysis(df_prep.copy(), tbl)