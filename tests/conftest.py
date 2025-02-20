import pytest
from dokker import mirror, Deployment
import os
from koil.composition import Composition
from fluss_next.fluss import Fluss
from rath.links.auth import ComposedAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.sign_local_link import ComposedSignTokenLink
from rath.links.graphql_ws import GraphQLWSLink
from fluss_next.fluss import Fluss
from fluss_next.rath import (
    FlussRath,
    SplitLink,
    FlussLinkComposition,
)
from graphql import OperationType

project_path = os.path.join(os.path.dirname(__file__), "integration")
private_key = os.path.join(project_path, "private_key.pem")


async def payload_retriever(o):
    return {"sub": 1}

@pytest.fixture(scope="session")
def deployed_app() -> Fluss:


    setup = mirror(project_path)
    setup.project.overwrite = True
    setup.add_health_check(
        url="http://localhost:8456/ht", service="mikro", timeout=5, max_retries=10
    )



    y = FlussRath(
        link=FlussLinkComposition(
            auth=ComposedSignTokenLink(
                private_key=private_key,
                payload_retriever=payload_retriever
            ),
            split=SplitLink(
                left=AIOHttpLink(endpoint_url="http://localhost:8456/graphql"),
                right=GraphQLWSLink(ws_endpoint_url="ws://localhost:8456/graphql"),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        ),
    )

    fluss = Fluss(
        rath=y,
    )

    with setup:
            
        setup.up()
        
        setup.check_health()

            
        with fluss as m:
            yield fluss


        setup.down()





