# load csv file

import csv
import json

with open("data.csv", "r") as f:
    with open("out.csv", "w") as f2:
        reader = csv.reader(f)
        writer = csv.writer(f2)
        writer.writerow(["prompt", "completion"])
        keys = None

        for row in reader:
            if keys is None:
                keys = row
                continue
            dic = {}
            for i in range(len(keys)):
                dic[keys[i]] = row[i]
            sub = dic["subject"].replace('"', "").replace("'", "").replace("　", " ")
            sender = dic["sender"].replace('"', "").replace("'", "").replace("　", " ")
            snipet = dic["snippet"].replace('"', "").replace("'", "").replace("　", " ")
            prompt = (
                f"title: {sub}\\nfrom: {sender}\\nsnippet: {snipet}\\n\\n\\n###\\n\\n"
            )
            completion = f'判定: {dic["ans"].split(", ")[0]}\\n理由: {dic["ans"].split(", ")[1]}\\n END'

            writer.writerow([prompt, completion])
