"""Strucutre Registration"""

try:
    from rekuest_next.structures.default import (
        get_default_structure_registry,
        PortScope,
        id_shrink,
    )
    from rekuest_next.widgets import SearchWidget

    from fluss_next.api.schema import (
        FlowFragment,
        SearchFlowsQuery,
        aget_flow,
        RunFragment,
        arun,
        SearchRunsQuery,
    )

    structure_reg = get_default_structure_registry()
    structure_reg.register_as_structure(
        FlowFragment,
        identifier="@fluss/flow",
        scope=PortScope.GLOBAL,
        aexpand=aget_flow,
        ashrink=id_shrink,
        default_widget=SearchWidget(query=SearchFlowsQuery.Meta.document, ward="fluss"),
    )
    structure_reg.register_as_structure(
        RunFragment,
        identifier="@fluss/run",
        scope=PortScope.GLOBAL,
        aexpand=arun,
        ashrink=id_shrink,
        default_widget=SearchWidget(query=SearchRunsQuery.Meta.document, ward="fluss"),
    )

except ImportError:
    raise e
    structure_reg = None


try:
    from fluss_next.arkitekt import builder
    from arkitekt_next.service_registry import get_default_service_builder_registry
    from arkitekt_next.model import Requirement

    service_builder_registry = get_default_service_builder_registry()
    service_builder_registry.register("fluss", builder, Requirement("arkitekt_fluss_next", "0.1.0"))

except ImportError as e:
    raise e
    service_builder_registry = None