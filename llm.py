from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings

load_dotenv()

llm = Gemini(model_name="models/gemini-pro")
Settings.llm = llm

from prompts import new_prompt, instruction_str, context
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from utils import save_json

recetas1_path = os.path.join("data", "recetas1.csv")
recetas1_df = pd.read_csv(recetas1_path)

recetas1_query_engine = PandasQueryEngine(
    df=recetas1_df, verbose = True, instruction_str=instruction_str
)

recetas1_query_engine.update_prompts({"pandas_prompt": new_prompt})

tools = [
    QueryEngineTool(
        query_engine=recetas1_query_engine,
        metadata=ToolMetadata(
            name="recipes_data",
            description="This gives recipes that match the given ingredients, and how to cook them"
        )
    )
]

agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

def get_recipes(ingredients_list):
    try:
        result = agent.query(f"{ingredients_list}")
    except:
        result = "No results or an error occurred"

    dic_result = {
        "answer": f"{result}"
    }
    return dic_result