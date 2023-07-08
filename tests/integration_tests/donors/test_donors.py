import pytest

from tests.conftest import ClientContext, DbContext

@pytest.mark.t
class TestDonors:
    @pytest.mark.parametrize(
        "nome, quantidade, indicacao",    
        [
            ('Nome', 5.0, 'Indicaçao'),
        ]
    )
    def test_add_donor(self, nome, quantidade, indicacao):
        client = ClientContext().client
        response = client.post(
            "/donors",
            json={
                "nome": nome,
                "quantidade": quantidade,
                "indicacao": indicacao,
            },
        )
        print(response)
        