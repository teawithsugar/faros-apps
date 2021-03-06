from datetime import datetime
from faros.client import FarosClient


def days_diff(date_string):
    return (datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ") - datetime.utcnow()).days


def lambda_handler(event, context):
    client = FarosClient.from_event(event)
    cutoff = int(event["params"]["days_left"])
    if cutoff < 1:
        raise ValueError("Days left should be a positive integer")

    query = '''{
              aws {
                acm {
                  certificateDetail {
                    data {
                      farosAccountId
                      farosRegionId
                      certificateArn
                      notAfter
                    }
                  }
                }
              }
            }'''

    response = client.graphql_execute(query)
    certificates = response["aws"]["acm"]["certificateDetail"]["data"]
    return [c for c in certificates if days_diff(c["notAfter"]) < cutoff]
