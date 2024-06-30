from dotenv import load_dotenv
import os
import time
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
            description="This returns recipes that match the given a 'ingredients list' and not matches the 'blacklisted list', and how to cook them, send the input in string format."
        )
    )
]

agent = ReActAgent.from_tools(tools, llm=llm, verbose=False, context=context)

def get_recipes(ingredients_list, blacklisted_ingredients, max_retries=3, retry_delay=0):
    if max_retries <= 0:
        dic_result = {
                "error": "Max retries is lower or equal than zero"
        }
        return dic_result

    filtered_list = remove_blacklisted(ingredients_list, blacklisted_ingredients)

    if len(filtered_list) <= 0:
        dic_result = {
                "error": "There's no ingredients or all of them are blacklisted"
        }
        return dic_result

    success = False
    attempts = 0

    while not success and attempts < max_retries:
        attempts += 1
    
        try:
            result = agent.query(f"ingredients list={filtered_list} blacklisted ingredients={blacklisted_ingredients}")
            success = True
        except Exception as e:
            result = "An error occurred with the Gemini AI api server"
            time.sleep(retry_delay)

    dic_result = {
        "answer" if success else "error": f"{result}"
    }

    return dic_result

def remove_blacklisted(ingredients_list, blacklisted_ingredients):
    blacklisted_set = set(blacklisted_ingredients)
    
    filtered_list = [ingredient for ingredient in ingredients_list if ingredient not in blacklisted_set]
    
    return filtered_list
