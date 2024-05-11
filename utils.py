import os

def save_json(json_result):
    output_file = os.path.join(".", "output.json")

    if not os.path.exists(output_file):
        open(output_file, "w")

    with open(output_file, "a") as f:
        f.writelines(str([json_result]) + "\n")

    return "json saved"