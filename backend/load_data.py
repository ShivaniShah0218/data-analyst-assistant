import pandas as pd
from .agent import AgentState


def load_data_node(state):
    df=pd.read_csv(state['file_path'])
    state["data"]=df
    state["preprocessing_steps"].append("data_loaded")
    return state
