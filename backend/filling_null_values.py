import pandas as pd
from .agent import AgentState


def handle_missing_values_node(state:AgentState) -> AgentState:
    data=state["data"]
    if isinstance(data, pd.DataFrame):
        data=data.fillna(data.mean(numeric_only=True))
        categorical_cols=data.select_dtypes(include=['object','category']).columns
        for col in categorical_cols:
            data[col].fillna("Other", inplace=True)
        state["data"]=data
        state["preprocessing_steps"].append("handled_missing_data")
    return state



