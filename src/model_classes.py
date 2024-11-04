from typing import Any
from pandas import DataFrame
from typing import Dict
from typing import List
from typing import Tuple

import pandas as pd
import numpy as np
import os
from scipy.stats import chi2_contingency

package_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.abspath(os.path.join(package_dir, ".."))

class Ingest:
    
    """
    Class to ingest dataframe input.
    """
    
    def __init__(
        self,
        config: Dict[Any, Any]
    ) -> None:
        
        """
        Inits class with the config file
        and unpacks the config file.
        """
        
        self.config = config
        
        self.unpack_config()

        
    def run(
        self
    ) -> DataFrame:
        
        """
        Run function for the class.
        
        :param None:
        :return df:
            DataFrame, ingested df
        """
        
        df = self.run_load()
        
        df = self.run_harmonize(df)
        
        return df
        
        
    def unpack_config(
        self
    ) -> None:
        
        """
        Function to unpack config vars.
        
        :var filepath:
            str, the relative filepath 
        :var group_variable:
            str, the column name for the 
            group variable of interest e.g.
            gender, which contains the target 
            class and non-target class e.g.
            females and males.
        :var group_target_val:
            str, within the group_variable column,
            contains the contains the target 
            class value e.g.
            females.
        :var group_other_val:
            str, within the group_variable column,
            contains the contains the non-target 
            class value e.g. males.
        :var outcome_variable:
            str, the column name for the 
            outcome variable of interest e.g.
            hired, which contains the target 
            class and non-target class e.g.
            hired and not-hired.
        :var outcome_target_val:
            str, within the outcome_variable column,
            contains the contains the target 
            class value e.g.
            hired.
        :var outcome_other_val:
            str, within the outcome_variable column,
            contains the contains the non-target 
            class value e.g. not-hired.
        :var grpers:
            str, the analysis group
            e.g. job_title.
        :var grpers_val:
            str, the value of the analysis group,
            e.g. analyst.
        """
        
        config = self.config
        
        try:
            self.filepath: str = config["Ingest"]["filepath"]
            self.group_variable: str = config["Ingest"]["group_variable"]
            self.group_target_val: str = config["Ingest"]["group_target_val"]
            self.group_other_val: str = config["Ingest"]["group_other_val"]
            self.outcome_variable: str = config["Ingest"]["outcome_variable"]
            self.outcome_target_val: str = config["Ingest"]["outcome_target_val"]
            self.outcome_other_val: str = config["Ingest"]["outcome_other_val"]
            self.grpers: str = config["Ingest"]["grpers"]
            self.grpers_val: str = config["Ingest"]["grpers_val"]

            # Type validation
            if not isinstance(self.filepath, str):
                raise TypeError("Expected 'filepath' to be of type 'str'.")
            if not isinstance(self.group_variable, str):
                raise TypeError("Expected 'group_variable' to be of type 'str'.")
            if not isinstance(self.group_target_val, str):
                raise TypeError("Expected 'group_target_val' to be of type 'str'.")
            if not isinstance(self.group_other_val, str):
                raise TypeError("Expected 'group_other_val' to be of type 'str'.")
            if not isinstance(self.outcome_variable, str):
                raise TypeError("Expected 'outcome_variable' to be of type 'str'.")
            if not isinstance(self.outcome_target_val, str):
                raise TypeError("Expected 'outcome_target_val' to be of type 'str'.")
            if not isinstance(self.outcome_other_val, str):
                raise TypeError("Expected 'outcome_other_val' to be of type 'str'.")
            if not isinstance(self.grpers, str):
                raise TypeError("Expected 'grpers' to be of type 'str'.")
            if not isinstance(self.grpers_val, str):
                raise TypeError("Expected 'grpers_val' to be of type 'str'.")
                
        except KeyError as e:
            raise KeyError(f"Missing key '{e.args[0]}' in the config file. "
                           "Please ensure the config file contains all required keys under the 'Ingest' section: "
                           "'filepath', 'group_variable', 'group_target_val', 'group_other_val', "
                           "'outcome_variable', 'outcome_target_val', 'outcome_other_val', 'grpers', and 'grpers_val'.")

        except TypeError as e:
            raise TypeError(f"Config file error: {e}")
        
    def run_load(
        self
    ) -> DataFrame:
        
        """
        Loads csv file. Assumes headers are row 0.
        
        :param None:
        :return DataFrame:
        """
        
        filepath = self.filepath
        csv_fp = os.path.join(main_dir, filepath)

        try:
            return pd.read_csv(csv_fp, skiprows=0)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"The file at {csv_fp} was not found. Please check the file path."
            )

        except pd.errors.EmptyDataError:
            raise ValueError(
                f"The file at {csv_fp} is empty and cannot be loaded."
            )

        except pd.errors.ParserError:
            raise ValueError(
                f"The file at {csv_fp} contains malformed data and could not be parsed as a valid CSV."
            )

        except PermissionError:
            raise PermissionError(
                f"Permission denied when attempting to read the file at {csv_fp}."
                f"Please check the file permissions."
            )

        except Exception as e:
            raise Exception(
                f"An unexpected error occurred while loading the file: {str(e)}"
            )
        
    def run_harmonize(
        self,
        df: DataFrame
    ) -> DataFrame:        

        """
        Function to harmonize the dataset.
        
        :param df: 
            DataFrame, loaded df
        :return df:
            DataFrame, filtered down to target and other group and
            harmonize the fields
        """
    
        group_variable = self.group_variable
        group_target_val = self.group_target_val
        group_other_val = self.group_other_val
        outcome_variable = self.outcome_variable
        outcome_target_val = self.outcome_target_val
        outcome_other_val = self.outcome_other_val
        grpers = self.grpers
        grpers_val = self.grpers_val

        df = self._apply_filters(
            df=df,
            group_variable=group_variable,
            group_target_val=group_target_val,
            group_other_val=group_other_val,
            grpers=grpers,
            grpers_val=grpers_val
        )
        
        df = self._apply_harmonize(
            df=df,
            group_variable=group_variable,
            group_target_val=group_target_val,
            group_other_val=group_other_val,
            outcome_variable=outcome_variable,
            outcome_target_val=outcome_target_val,
            outcome_other_val=outcome_other_val
        )
      
        return df
    
    def _apply_filters(
        self,
        df: DataFrame,
        group_variable: str,
        group_target_val: str,
        group_other_val: str,
        grpers: str,
        grpers_val: str
    ) -> DataFrame:
        
        """
        Method to apply filters.
        
        :param df:
            DataFrame, target df
        :param group_variable:
            str, column name of the
            target variable
        :param group_target_val:
            str, class target value of the group_variable
            aka the protected class value
        :param group_other_val:
            str, class nontarget value of the group_variable
            aka the nonprotected class value
        :param grpers:
            str, the name of the analysis group.
        :param grpers_val:
            str, the value of the analysis group.
        :return df:
            DataFrame, filtered df
        """
                
        df = df.loc[
            df[group_variable].isin(
                [
                    group_target_val, 
                    group_other_val
                ]
            )
        ]  
            
        df = df.loc[
            df[grpers]==grpers_val
        ]
            
        return df
    
    def _apply_harmonize(
        self,
        df: DataFrame,
        group_variable: str,
        group_target_val: str,
        group_other_val: str,
        outcome_variable: str,
        outcome_target_val: str,
        outcome_other_val: str
    ) -> DataFrame:
        
        """
        Method to harmonize targets.
        
        :param df:
            DataFrame, target df
        :param group_variable:
            str, column name of the
            target variable
        :param group_target_val:
            str, class target value of the group_variable
            aka the protected class value
        :param group_other_val:
            str, class nontarget value of the group_variable
            aka the nonprotected class value     
        :param outcome_variable:
            str, the column name of the outcome 
        :param outcome_target_val:
            str, class target value of the outcome_variable
            aka success
        :param outcome_other_val:
            str, class nontarget value of the outcome_variable
        :return df:
            DataFrame, target df
        """
        
        # harmonize the group target
        df['group_var_clean'] = np.where(
            df[group_variable]==group_target_val, 
            1,
            np.where(
                df[group_variable]==group_other_val, 
                0, 
                -1
            )
        )
        
        # harmonize the outcome target
        df['outcome_var_clean'] = np.where(
            df[outcome_variable]==outcome_target_val, 
            1,  
            np.where(
                df[self.outcome_variable]==outcome_other_val,
                0, 
                -1
            )
        )  
        
        return df
    
    
class Transform:
    
    """
    Class to transform dataframe inputs into 
    2x2 contingency table.
    """
    
    def __init__(
        self, 
        df: DataFrame
    ) -> None:
        
        """
        :param df:
            DataFrame, input df
        """
    
        self.df = df
    
    def run_build_cont_table(
        self
    ) -> List[int]:
        
        """
        Function to generate contingency table format.
        
        Places the target group val in the top row and the
        target group other to the bottom row.
        
        Places no-success outcome on the first column and success
        on the second column.
        
        :return tbl:
            List[int], filtered down to target and other group.
        """
        
        df = self.df
        
        cols = [
            'group_var_clean', 
            'outcome_var_clean'
        ]
        
        df = df[cols]
        
        tbl = (
            df.pivot_table(
                index='group_var_clean',
                columns='outcome_var_clean', 
                aggfunc=len
            ).
            sort_index(
                axis=1, 
                ascending=True
            ).
            sort_index(ascending=False). # ensure always [1,0]
            values.tolist()
        ) 
                    
        return tbl
        
class StatsTesting2x2Cont:
    
    """
    Class to perform 2x2 Contigency Table analysis
    with Chi2 and Phi Correlation Coefficent Testing.

    Provides context into potential association between
    variables and the strength of the association.
    """
    
    def __init__(
        self,
        config: Dict[Any, Any],
        tbl: List[int],
        df: DataFrame
    ) -> None:
        
        """
        Inits the class variables and unpacks the
        config variables.
        
        :param config:
            Dict[str,Any], loaded config file.
        :param tbl:
            List[int], 2x2 cont table.
        :param df:
            DataFrame, original input DataFrame.
        """
        
        self.config = config
        self.tbl = tbl
        self.df = df

        self.unpack_config()

    def run_testing(
        self
    ) -> DataFrame:
        
        """
        Run function for the class.
        
        Runs hypothesis evaluation and builds
        the output report DataFrame.
        
        :param None:
        :return df_results:
            DataFrame, with testing results.
        """
        
        alpha = self.alpha
        tbl = self.tbl
        process = self.process
        group_variable = self.group_variable
        group_target_val = self.group_target_val
        group_other_val = self.group_other_val
        bin_edges = self.bin_edges
        bin_labels = self.bin_labels
                
        res = self.gen_hypothesis_eval(tbl)

        df_results = self.run_report_bld(
            alpha=alpha,
            res=res,
            tbl=tbl,
            process=process,
            group_variable=group_variable,
            group_target_val=group_target_val,
            group_other_val=group_other_val,
            bin_edges=bin_edges,
            bin_labels=bin_labels
        )
        
        return df_results
    
    def unpack_config(
        self
    ) -> None:
        
        """
        Function to unpack config variables.
        
        :param None:
        :return None:
        """
        
        config = self.config

        try:
            self.alpha: float = config["StatsTesting2x2Cont"]["alpha"]
            self.group_variable: str = config["Ingest"]["group_variable"]
            self.group_target_val: str = config["Ingest"]["group_target_val"]
            self.group_other_val: str = config["Ingest"]["group_other_val"]
            self.outcome_variable: str = config["Ingest"]["outcome_variable"]
            self.outcome_target_val: str = config["Ingest"]["outcome_target_val"]
            self.outcome_other_val: str = config["Ingest"]["outcome_other_val"]
            self.grpers: str = config["Ingest"]["grpers"]
            self.grpers_val: str = config["Ingest"]["grpers_val"]
            
            self.testing: str = config["StatsTesting2x2Cont"]["testing"]
            self.process: str = config["StatsTesting2x2Cont"]["process"]
            self.bin_edges: List[float] = config["StatsTesting2x2Cont"]["phi_bin_edges"]
            self.bin_labels: List[str] = config["StatsTesting2x2Cont"]["phi_bin_labels"]

            if not isinstance(self.alpha, float):
                raise TypeError("Expected 'alpha' to be of type 'float'.")
            if not isinstance(self.group_variable, str):
                raise TypeError("Expected 'group_variable' to be of type 'str'.")
            if not isinstance(self.group_target_val, str):
                raise TypeError("Expected 'group_target_val' to be of type 'str'.")
            if not isinstance(self.group_other_val, str):
                raise TypeError("Expected 'group_other_val' to be of type 'str'.")
            if not isinstance(self.outcome_variable, str):
                raise TypeError("Expected 'outcome_variable' to be of type 'str'.")
            if not isinstance(self.outcome_target_val, str):
                raise TypeError("Expected 'outcome_target_val' to be of type 'str'.")
            if not isinstance(self.outcome_other_val, str):
                raise TypeError("Expected 'outcome_other_val' to be of type 'str'.")
            if not isinstance(self.grpers, str):
                raise TypeError("Expected 'grpers' to be of type 'str'.")
            if not isinstance(self.grpers_val, str):
                raise TypeError("Expected 'grpers' to be of type 'str'.")
            if not isinstance(self.testing, str):
                raise TypeError("Expected 'testing' to be of type 'str'.")
            if not isinstance(self.process, str):
                raise TypeError("Expected 'process' to be of type 'str'.")
            if not isinstance(
                self.bin_edges, list
            ) or not all(
                isinstance(
                    i, (int, float)
                ) for i in self.bin_edges
            ):
                raise TypeError("Expected 'bin_edges' to be a list of floats.")
            if not isinstance(
                self.bin_labels, list
            ) or not all(
                isinstance(i, str) for i in self.bin_labels
            ):
                raise TypeError("Expected 'bin_labels' to be a list of strings.")
        
        except KeyError as e:
            raise KeyError(
                f"Missing key '{e.args[0]}' in the config file. "
                f"Ensure all required keys are present in the 'Ingest' and 'StatsTesting2x2Cont' sections."
            )

        except TypeError as e:
            raise TypeError(f"Config file error: {e}")

        
    def gen_hypothesis_eval(
        self,
        tbl: List[int]
    ) -> chi2_contingency:
        
        """
        Function to generate the chi2_contigency
        statistic and result.
        """
        
        #size = np.shape(tbl)
        #tbl_len = len(tbl)
        
        res = chi2_contingency(
            tbl
        )
            
        return res
        
    def run_report_bld(
        self,
        alpha: float,
        res: chi2_contingency,
        tbl: List[int],
        process: str,
        group_variable: str,
        group_target_val: str,
        group_other_val: str,
        bin_edges: List[float],
        bin_labels: List[str]
    ) -> DataFrame:
        
        """
        Runs report for statistical testing
        chi2_contingency results
        
        :param alpha:
            float, alpha value for significance evaluation.
        :param res:
            chi2_contingency, result of the chi2_contingency.
        :param tbl:
            List[int], the contingency table.
        :param process: 
            str, the name of the business process
            being tested, e.g. 'hiring'.
        :param group_variable:
            str, column name of the
            target variable.
        :param group_target_val:
            str, class target value of the group_variable
            aka the protected class value.
        :param group_other_val:
            str, class nontarget value of the group_variable
            aka the nonprotected class value.  
        :param bin_edges:
            List[float], edges for phi
            bins.
        :param bin_labels:
            List[str], labels for the phi
            bins.
        :return df:
            DataFrame, target
        """
        
        pvalue = res[1]
        
        df = pd.DataFrame()

        df = self._gen_significance_test(
            df=df,
            pvalue=pvalue,
            alpha=alpha
        )
        
        (
            df,
            A,
            B,
            C,
            D,
            total_target_grp,
            total_non_target_grp,
            diagonals,
            percent_target_succ,
            percent_non_target_succ,
            phi_numerator,
            phi_denominator
        ) = self._gen_table_calcs(
                df=df,
                tbl=tbl,
        )
        
        if res[1] <= alpha:
            df, phi_result = self._gen_phi_coefficient(
                df=df,
                tbl=tbl,
                bin_edges=bin_edges,
                bin_labels=bin_labels,
                process=process,
                group_variable=group_variable,
                group_target_val=group_target_val,
                group_other_val=group_other_val,
                diagonals=diagonals,
                numerator=phi_numerator,
                denominator=phi_denominator,
                percent_target_succ=percent_non_target_succ,
                percent_non_target_succ=percent_non_target_succ,
            )
            
        else:
            df['phi_corr_coeff'] = np.nan
            df['phi_bins'] = np.nan
            
            phi_result = ""
        
        df = self._gen_four_fifths_test(
            df,
            percent_target_succ=percent_non_target_succ,
            percent_non_target_succ=percent_non_target_succ
        )
                
        df = self._gen_outcome_meta(
            df,
            round(res[1],3),
            phi_result,
        )
        
        df = self._gen_unpack_stats(
            df,
            res,
            tbl,
            alpha
        )
        
        return df
        
    def _gen_unpack_stats(
        self,
        df: DataFrame,
        res: chi2_contingency,
        tbl: List[float],
        alpha: float
    ) -> DataFrame:
        
        """
        Method to unpack test stats from
        chi2_contingency results.
        
        :param df:
            DataFrame, output df.
        :param res:
            chi2_contingency, results array.
        :return df:
            DataFrame, output df.
        """
        
        group_target_val = self.group_target_val
        group_other_val = self.group_other_val
        outcome_target_val = self.outcome_target_val
        outcome_other_val = self.outcome_other_val
        
        rows = [group_target_val] + [group_other_val]
        cols = [outcome_other_val] + [outcome_target_val]
    
        df['statistic'] = res[0]
        df['pvalue'] = res[1]
        df['alpha'] = alpha
        df['dof'] = res[2]
        df['tbl_rows'] = [rows]
        df['tbl_cols'] = [cols]
        df['tbl'] = [tbl]
        df['expected_freq'] = [res[3]]
        df['tbl_expected_diff'] = [tbl - res[3]]
        
        return df
    
    def _gen_significance_test(
        self,
        df: DataFrame,
        pvalue: float,
        alpha: float
    ):
        """
        Method to report on test significance.
        
        :param df:
            DataFrame, results df.
        :param pval:
            int, pvalue.
        :param alpha:
            float, the alpha value for testing eval.
        :return df:
            DataFrame with metadata added.     
        """
            
        if pvalue <= alpha:
            val = 'Statistically significant result'
            
        else:
            val = 'No statistically significant result'
                    
        df['test_result'] = [val]
        
        return df
    
    def _gen_phi_coefficient(
        self,
        df: DataFrame,
        tbl: List[int],
        process: str,
        group_variable: str,
        group_target_val: str,
        group_other_val: str,
        bin_edges: List[float],
        bin_labels: List[str],
        diagonals: List[float],
        numerator: float,
        denominator: float,
        percent_target_succ: float,
        percent_non_target_succ: float,
    ) -> DataFrame:
        
        """
        Method to generate the phi coefficient.
        
        :param df:
            DataFrame, the results df.
        :param tbl:
            List[int], the 2x2 cont table.
        :param process: 
            str, the name of the business process
            being tested, e.g. 'hiring'.
        :param group_variable:
            str, column name of the
            target variable.
        :param group_target_val:
            str, class target value of the group_variable
            aka the protected class value.
        :param group_other_val:
            str, class nontarget value of the group_variable
            aka the nonprotected class value.  
        :param bin_edges:
            List[float], edges for phi
            bins.
        :param bin_labels:
            List[str], lab
        :return df:
            DataFrame, output df.
        """
        phi = numerator / denominator if denominator != 0 else 0

        df['phi_corr_coeff'] = phi
                
        df = self._gen_prep_phi_bins(
            df=df,
            bin_edges=bin_edges,
            bin_labels=bin_labels
        )

        df, phi_result = self._gen_prep_diagonals(
            df=df,
            diagonals=diagonals,
            process=process,
            group_variable=group_variable,
            group_other_val=group_other_val,
            group_target_val=group_target_val,
            percent_non_target_succ=percent_non_target_succ,
            percent_target_succ=percent_target_succ,
        )
        
        return df, phi_result
    
    def _gen_table_calcs(
        self,
        df: DataFrame,
        tbl: List[int]
    ) -> Tuple[
        DataFrame, float, float, float, float,
        float, float, float, float, 
        float, float, float
    ]:
        
        """
        Method to generate phi bins. Provides additional
        explainability on the magnitude of association, when 
        an association is found.
        
        :param df:
            DataFrame, output df.
        :param tbl:
            List[int], 2x2 contingency.
        :return [
            df, A, B, C, D, total_target_grp,
            total_non_target_grp, diagonals,
            percent_target_succ, percent_non_target_succ,
            phi_numerator, phi_denominator
        ]:
            Tuple[DataFrame, float, float, float, float,
        float, float, float, float, 
        float, float, float
        ]
        """
        
        # females, males; no succ, succ
        A, B = tbl[0] 
        C, D = tbl[1]
        
        total_target_grp = A + B
        total_non_target_grp = C + D
        diagonals = (A + D) > (B + C)
        percent_target_succ = (B / total_target_grp) * 100
        percent_non_target_succ = (D / total_non_target_grp) * 100
        phi_numerator = (A * D) - (B * C)
        phi_denominator = np.sqrt((A + B) * (C + D) * (A + C) * (B + D))      
           
        return (
            df,
            A,
            B,
            C,
            D,
            total_target_grp,
            total_non_target_grp,
            diagonals,
            percent_target_succ,
            percent_non_target_succ,
            phi_numerator,
            phi_denominator
        )
    
    def _gen_prep_phi_bins(
        self,
        df: DataFrame,
        bin_edges: List[float],
        bin_labels: List[str]
    ) -> DataFrame:
        
        """
        Method to generate pandas bins for 
        phi coeff.
        
        :param df:
            DataFrame, output df.
        :param bin_edges:
            List[float], edges for phi
            bins.
        :param bin_labels:
            List[str], labels for the phi
            bins.
        :return df:
            DataFrame, output df.
        """
    
        df['phi_bins'] = pd.cut(
            df['phi_corr_coeff'], 
            bins=bin_edges, 
            labels=bin_labels, 
            include_lowest=True
        )
        
        return df
    
    def _gen_four_fifths_test(
        self,
        df: DataFrame,
        percent_target_succ: float,
        percent_non_target_succ: float
    ) -> DataFrame:
        
        ratio = percent_target_succ / percent_non_target_succ
        
        if ratio < .8:
            ratio_desc = f'4/5ths Test failed at ratio of: {round(ratio,3)}.'
        elif ratio >= .8:
            ratio_desc = f'4/5ths Test passed at a ratio of: {round(ratio,3)}.'
        else:
            ratio_desc = 'Error calculating 4/5 Test'
        
        df['four_fifths_test'] = ratio_desc
        return df
    
    def _gen_prep_diagonals(
        self,
        df: DataFrame,
        diagonals: bool,
        process: str,
        group_variable: str,
        group_other_val: str,
        group_target_val: str,
        percent_non_target_succ: float,
        percent_target_succ: float,
    ) -> Tuple[DataFrame, str]:
        
        """
        Method to generate the magnitude of the
        assocation using phi coefficient analysis.
        
        :param df:
            DataFrame, output df.
        :param diagonals:
            bool,
        :param process: 
            str, the name of the business process
            being tested, e.g. 'hiring'.
        :param group_variable:
            str, column name of the
            target variable.
        :param group_target_val:
            str, class target value of the group_variable
            aka the protected class value.
        :param group_other_val:
            str, class nontarget value of the group_variable
            aka the nonprotected class value.   
        :param percent_non_target_succ:
            float, the success percentage attained
            for the the non-target group.
        :param percent_target_succ:
            float, the success percentage attained for the
            target class.
        :return (df, phi_col):
            Tuple[df, phi_col]
        """
        
        phi_bin = df['phi_bins'].values[0]    
        phi_corr_coeff = df['phi_corr_coeff'].values[0]    

        if diagonals:
            diagonal_msg = (
                f"The values on the positive diagonal of the 'tbl' indicate the distribution of {process} success across {group_variable} categories.\n\n"
                f"{group_other_val} had a higher proportion of successful outcomes compared to {group_target_val}.\n\n"
                f"Specifically, {percent_non_target_succ:.1f}% of {group_other_val} had success while only {percent_target_succ:.1f}%"
                f" of {group_target_val} had success.\n\n"
                f"This significant difference in {process} success rates suggests a potential {group_variable} bias, with {group_other_val} success in {process}"
                f" at a higher rate than {group_target_val}."
            )
            phi_col = f"The phi correlation coefficient is {phi_corr_coeff:.3f}, indicating a {phi_bin} effect size. {diagonal_msg}"
            
        else:
            diagonal_msg = "The diagonal values are not substantially higher, suggesting the relationship might be more nuanced."
            phi_col = diagonal_msg
            
        return df, phi_col
    
    def _gen_outcome_meta(
        self,
        df: DataFrame,
        pval: float,
        phi_result: str
    ) -> DataFrame:
        
        """
        Method to generate meta data for 
        reporting dataframe
        
        :param df:
            DataFrame, results df
        :param pval:
            int, pvalue
        :param phi_result:
            str, result of phi testing.
        :return df:
            DataFrame with metadata added
        """
        
        grpers = self.grpers
        grpers_val = self.grpers_val
        result = df['test_result'].values[0]
        phi_col = df['phi_corr_coeff'].values[0]
        testing = self.testing
        process = self.process
        group_target_val = self.group_target_val
        alpha = self.alpha
        four_fifths = df['four_fifths_test'].values[0]
        


        if result == "Statistically significant result":
            col = f"Testing for {grpers}: {grpers_val}, {four_fifths}\n\nBased on the results of the chi-square test of independence, there is {result} for {testing}-based {process} discrimination against {group_target_val} at the chosen significance level of {alpha}.\n\n"
            col = f"{col}{phi_result}"
        else: 
            col = ""
                
        df['result_desc'] = col
        
        return df