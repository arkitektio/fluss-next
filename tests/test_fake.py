import pytest
from fluss_next.api.schema import get_flow



@pytest.mark.asyncio
def test_fake(deployed_app):

    x = get_flow(id=3)
    
