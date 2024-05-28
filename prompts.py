from llama_index.core import PromptTemplate

instruction_str= """\
    1. Make from the query from the list of ingredients and the list of blacklisted ingredients, get these list from the dic keys 'ingredients list' and 'blacklisted list'.
    2. Convert the query to executable Python code using Pandas.
    3. The final line of code should be a Python expression that can be called with the 'eval()' function.
    4. The code should represent a solution to the query.
    5. PRINT ONLY THE EXPRESSION
    6. Do not quote the expression.
    7. The Query should be in the "ingredients" column using the ingredients.str.contains('...') function if it's in the list of ingredients or ~ingredients.str.contains('...') if in the list of blacklisted ingredients.
    8. The Query should return both the "Title" and the "Instructions" columns that matches the expression expression in the last item.
"""

new_prompt = PromptTemplate(
    """\
    You are working with a pandas dataframe in Python.
    The name of the dataframe is 'df'
    
    Follow this instructions:
    {instruction_str}
    Query: {query_str}

    Expression: """
)

context = """Purpose: The primary role of this agent is to assist users by receiving a list of ingredients that they have and a list of blacklisted ingredients, and replying to them with 3 random recipes they can cook. For this the agent should translate the context of each list from spanish to english, and then use the tools to locate recipes that CONTAINS some of the list of ingredients the user provided and NOT CONTAINS the blacklisted ingredients. Return both their names and instructions for 3 random recipes they can cook. Use the following json scheme for the reply: [ { \"titulo\" : \"titulo receta 1\", \"ingredientes\": \"lista de ingredientes receta 1\", \"pasos\" : \"lista de pasos a seguir para cocinar la receta 1\"}, { \"titulo\" : \"titulo receta 2\", \"ingredientes\": \"lista de ingredientes receta 2\", \"pasos\" : \"lista de pasos a seguir para cocinar la receta 2\"},...]. It's very important to follow this format.
"""