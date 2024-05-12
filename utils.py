import os
import json

def save_json(dic_result):
    output_file = os.path.join(".", "output.json")

    if not os.path.exists(output_file):
        open(output_file, "w")

    with open(output_file, "a") as f:
        json.dump(dic_result, f)

    return "json saved"