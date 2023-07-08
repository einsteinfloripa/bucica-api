import pytest

from tests.conftest import ClientContext
from src.models.donor_model import DonorModel

@pytest.mark.t
class TestDonors:
    @pytest.mark.parametrize(
        "nome, quantidade, indicacao, response_code",    
        [
            ('N', 5.0, 'Indicaçao', 422),
            ('Nome', 5.0, 'I', 422),
            ('Nome', -5.0, 'Indicaçao', 422),
            ('Nome', 5.0, 'Indicaçao', 201),
        ]
    )
    def test_add_donor_checks(self, nome, quantidade, indicacao, response_code):
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
        assert response.status_code == response_code
    
    @pytest.mark.parametrize(
        "nome, quantidade, indicacao",    
        [
            ('Nome', 5.0, 'Indicaçao'),
            ('segundo nome', 100000.0, 'Indicaçao a mil'),
        ]
    )
    def test_add_donor_updated_database(
            self, 
            nome: str,
            quantidade: float,
            indicacao: str,
            session,
        ):
        client = ClientContext().client
        response = client.post(
            "/donors",
            json={
                "nome": nome,
                "quantidade": quantidade,
                "indicacao": indicacao,
            },
        )
        
        donor_obj = session.query(DonorModel).filter(DonorModel.name == nome).first()
        assert donor_obj.name == nome
        assert donor_obj.amount == quantidade
        assert donor_obj.indication == indicacao