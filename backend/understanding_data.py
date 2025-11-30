import pandas as pd
from .agent import AgentState

def understanding_data_node(state:AgentState)->AgentState:
    data=state["data"]
    result={}
    if isinstance(data,pd.DataFrame):
        result["Data Shape"]=data.shape
        result["Data Size"]=data.size
        result["Number of Dimensions"]=data.ndim
        result["Column Names"]=list(data.columns)
        result["Index"]=list(data.index)
        result["Column Data Types"]=data.dtypes.to_string()
        result["Descriptive Statistics (Numerical)"]=data.describe().to_string()
        result["Descriptive Statistics (All Columns)"]=data.describe(include="all").to_string()
        result["Memory Usage (per column)"]=data.memory_usage(deep=True).to_string()
        result["Data Head (first 5 rows)"]=data.head().to_string()
        result["Data Structure Step"]="Before filling Null Values" if state["preprocessing_steps"][-1]=="data_loaded" else "After filling Null Values"
        state["info"].append(result)
        state["preprocessing_steps"].append("understanding_data")
    return state