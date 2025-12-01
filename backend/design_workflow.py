import pandas as pd
from .agent import AgentState
from .understanding_data import understanding_data_node
from .filling_null_values import handle_missing_values_node
from .anomaly_detection import anomaly_detection_node
from .load_data import load_data_node
from .pattern_detection import pattern_detection_node
from .llm_explanation import llm_explanation_node
from langgraph.graph import StateGraph, END


class AgentFlow_Design:
    def __init__(self):
        self.workflow=None
        self.app=None

    def decide_next_point(self,state:AgentState)-> str:
        if "handled_missing_data" in state["preprocessing_steps"]:
            return "pattern_detection"
        else:
            return "handle_missing_values"
        
    def noop(self,state: AgentState) -> dict:
        return {}

    def define_workflow(self):
        self.workflow=StateGraph(AgentState)
        self.workflow.add_node("load_data",load_data_node)
        self.workflow.add_node("understand_data",understanding_data_node)
        self.workflow.add_node("handle_missing_values",handle_missing_values_node)
        self.workflow.add_node("pattern_detection",pattern_detection_node)
        self.workflow.add_node("anomaly_detection",anomaly_detection_node)
        self.workflow.add_node("decide_next_point",self.noop)
        self.workflow.add_node("llm_explanation",llm_explanation_node)


        self.workflow.set_entry_point("load_data")
        self.workflow.add_edge("load_data","understand_data")
        self.workflow.add_edge("understand_data","decide_next_point")
        self.workflow.add_conditional_edges("decide_next_point",self.decide_next_point,{"pattern_detection":"pattern_detection","handle_missing_values":"handle_missing_values"})
        self.workflow.add_edge("handle_missing_values","understand_data")
        self.workflow.add_edge("pattern_detection","anomaly_detection")
        self.workflow.add_edge("anomaly_detection","llm_explanation")
        self.workflow.add_edge("llm_explanation",END)
        self.app=self.workflow.compile()
        return self.app
    







# initial_state= AgentState(file_path='../sample_test_data.csv',data= None,preprocessing_steps= [],info= [],error_message= "",anomalies= None,correlations= None)#, preprocessing_steps=[],error_message="", info=[])
# final_state= app.invoke(initial_state)

# print("Data Understanding Before handling missing values")
# print(final_state["info"][0])# if final_state["info"]["Data Structure Step"]=="Before filling Null Values" else "")
# print("Preprocessed Data:")
# print(final_state["data"])
# print("Data Understanding After handling missing values")
# print(final_state["info"][1])# if final_state["info"]["Data Structure Step"]=="After filling Null Values" else "")
# print("Pattern Detection:")
# print(final_state["correlations"])
# print("Anomaly Detection:")
# print(final_state["anomalies"])
# print("Data Analyst Explanation:")
# print(final_state["explanation"])
# print("Applied Preprocessing steps:")
# print(final_state["preprocessing_steps"])


