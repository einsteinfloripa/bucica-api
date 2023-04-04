"""change columns name

Revision ID: c30f103092b2
Revises: 0fa6e7b2f5e8
Create Date: 2023-03-19 08:43:30.565016

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c30f103092b2'
down_revision = '0fa6e7b2f5e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Cadastro_Alunos', sa.Column('nome', sa.String(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('telefone', sa.String(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('data_nascimento', sa.Date(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('estado_civil', sa.String(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('estado', sa.String(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('cidade', sa.String(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('bairro', sa.String(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('rua', sa.String(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('numero', sa.String(), nullable=False))
    op.add_column('Cadastro_Alunos', sa.Column('complemento', sa.String(), nullable=False))
    op.alter_column('Cadastro_Alunos', 'rg',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Cadastro_Alunos', 'cpf',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Cadastro_Alunos', 'cep',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Cadastro_Alunos', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('Cadastro_Alunos', 'neighborhood')
    op.drop_column('Cadastro_Alunos', 'name')
    op.drop_column('Cadastro_Alunos', 'street')
    op.drop_column('Cadastro_Alunos', 'state')
    op.drop_column('Cadastro_Alunos', 'civil_state')
    op.drop_column('Cadastro_Alunos', 'birthdate')
    op.drop_column('Cadastro_Alunos', 'complement')
    op.drop_column('Cadastro_Alunos', 'number')
    op.drop_column('Cadastro_Alunos', 'city')
    op.drop_column('Cadastro_Alunos', 'phone')
    op.add_column('Presenca', sa.Column('aluno_id', sa.Integer(), nullable=False))
    #op.add_column('Presenca', sa.Column('atraso', sa.Enum('on_time', 'half_late', 'late', name='latetypes'), nullable=True))
    op.add_column('Presenca', sa.Column('falta', sa.Boolean(), nullable=False))
    op.add_column('Presenca', sa.Column('criado_em', sa.DateTime(), nullable=True))
    op.drop_constraint('Presenca_student_id_fkey', 'Presenca', type_='foreignkey')
    op.create_foreign_key(None, 'Presenca', 'Cadastro_Alunos', ['aluno_id'], ['id'])
    op.drop_column('Presenca', 'datetime_of_creation')
    # op.drop_column('Presenca', 'late')
    op.drop_column('Presenca', 'absence')
    op.drop_column('Presenca', 'student_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Presenca', sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Presenca', sa.Column('absence', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # op.add_column('Presenca', sa.Column('late', postgresql.ENUM('on_time', 'half_late', 'late', name='late'), autoincrement=False, nullable=True))
    op.add_column('Presenca', sa.Column('datetime_of_creation', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Presenca', type_='foreignkey')
    op.create_foreign_key('Presenca_student_id_fkey', 'Presenca', 'Cadastro_Alunos', ['student_id'], ['id'])
    op.drop_column('Presenca', 'criado_em')
    op.drop_column('Presenca', 'falta')
    # op.drop_column('Presenca', 'atraso')
    op.drop_column('Presenca', 'aluno_id')
    op.add_column('Cadastro_Alunos', sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('city', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('complement', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('birthdate', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('civil_state', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('street', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Cadastro_Alunos', sa.Column('neighborhood', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('Cadastro_Alunos', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Cadastro_Alunos', 'cep',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Cadastro_Alunos', 'cpf',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Cadastro_Alunos', 'rg',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('Cadastro_Alunos', 'complemento')
    op.drop_column('Cadastro_Alunos', 'numero')
    op.drop_column('Cadastro_Alunos', 'rua')
    op.drop_column('Cadastro_Alunos', 'bairro')
    op.drop_column('Cadastro_Alunos', 'cidade')
    op.drop_column('Cadastro_Alunos', 'estado')
    op.drop_column('Cadastro_Alunos', 'estado_civil')
    op.drop_column('Cadastro_Alunos', 'data_nascimento')
    op.drop_column('Cadastro_Alunos', 'telefone')
    op.drop_column('Cadastro_Alunos', 'nome')
    # ### end Alembic commands ###
