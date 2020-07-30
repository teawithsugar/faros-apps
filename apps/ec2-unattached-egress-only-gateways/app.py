from faros.client import FarosClient


def lambda_handler(event, context):
    client = FarosClient.from_event(event)

    query = '''{
              aws {
                ec2 {
                  egressOnlyInternetGateway {
                    data {
                      farosAccountId
                      farosRegionId
                      egressOnlyInternetGatewayId
                      attachments {
                        vpcId
                      }
                    }
                  }
                }
              }
            }'''

    response = client.graphql_execute(query)
    gateways = response["aws"]["ec2"]["egressOnlyInternetGateway"]["data"]
    return [g for g in gateways if not g["attachments"]]
