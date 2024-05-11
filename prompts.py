from llama_index.core import PromptTemplate

instruction_str= """\
    1. Convert the query to executable Python code using Pandas.
    2. The final line of code should be a Python expression that can be called with the 'eval()' function.
    3. The code should represent a solution to the query.
    4. PRINT ONLY THE EXPRESSION
    5. Do not quote the expression.
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

context = """Purpose: The primary role of this agent is to assist users by receiving a list of ingredients that they have and replying
to them with 3 recipes they can cook, by returning a list of instructions of those recipes.
"""