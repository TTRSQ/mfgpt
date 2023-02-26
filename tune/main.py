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
            obj = {
                "title": dic["subject"],
                "from": dic["sender"],
                "snippet": dic["snippet"],
            }
            prompt = json.dumps(obj, ensure_ascii=False)
            completion = dic["ans"]

            writer.writerow([prompt, completion])
