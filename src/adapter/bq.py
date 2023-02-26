from dataclasses import dataclass
from typing import List, Optional
from google.cloud import bigquery
import os

table_id = os.environ.get("BQ_TABLE_ID")


@dataclass
class Row:
    id: str
    threadId: str
    snippet: Optional[str]
    timeStamp: Optional[int]


def insert_mails(mails: List[Row]):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    rows_to_insert = [m.__dict__ for m in mails]

    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def list_mails(search_ids: List[str]) -> List[Row]:
    client = bigquery.Client()

    query = f"""
    SELECT *
    FROM `{table_id}`
    WHERE id IN ({','.join([f'"{id}"' for id in search_ids])})
    LIMIT 1000
    """

    query_job = client.query(query)  # Make an API request.

    retMails = []
    for row in query_job:
        retMails.append(Row(row.id, row.threadId, row.snippet, row.timeStamp))
    return retMails
