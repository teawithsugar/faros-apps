from faros.client import FarosClient
from faros.utils import time_diff


def lambda_handler(event, context):
    client = FarosClient.from_event(event)
    cutoff = int(event["params"]["max_days"])

    query = '''{
              github {
                repository {
                  data {
                    name
                    created_at
                    updated_at
                  }
                }
              }
            }'''

    response = client.graphql_execute(query)
    repos = response["github"]["repository"]["data"]

    return [
        repo for repo in repos if time_diff(repo["updated_at"]).days > cutoff
    ]
