try:

    from .fluss import Fluss
    from .rath import FlussLinkComposition, FlussRath
    from rath.links.split import SplitLink
    from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
    from rath.contrib.fakts.links.graphql_ws import FaktsGraphQLWSLink
    from rath.contrib.herre.links.auth import HerreAuthLink
    from graphql import OperationType
    from herre import Herre
    from fakts import Fakts


    from arkitekt_next.service_registry import get_default_service_builder_registry, Params
    from arkitekt_next.model import Requirement


    class ArkitektNextFluss(Fluss):
        rath: FlussRath


    def build_arkitekt_next_fluss(herre: Herre, fakts: Fakts, params: Params):
        return ArkitektNextFluss(
            rath=FlussRath(
                link=FlussLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(fakts_group="fluss", fakts=fakts),
                        right=FaktsGraphQLWSLink(fakts_group="fluss", fakts=fakts),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            )
        )

    
        
    service_builder_registry = get_default_service_builder_registry()
    service_builder_registry.register("fluss", build_arkitekt_next_fluss, Requirement(
            service="live.arkitekt_next.fluss",
            description="An instance of ArkitektNext Fluss to make requests to the user's data",
        ))
    imported = True

except ImportError as e:

    imported = False
    raise e