type ErrorTypes = keyof typeof errorSchemas;

export function errorFactory(errorType: ErrorTypes) {
  return errorSchemas[errorType];
}

const errorSchemas = {
  error_matricula_vazia: {
    statusCode: 422,
    mensagem: "Você deve mandar a matrícula do aluno!",
  },
  error_matricula_nao_exite: {
    statusCode: 404,
    mensagem: "A matrícula fornecida não existente!",
  },
  error_final_semana: {
    statusCode: 400,
    mensagem: "Hoje é final de semana, não temos aula!",
  },
  error_presenca_ja_feita: {
    statusCode: 400,
    mensagem: "Já foi feito a presença do aluno hoje!",
  },
  error_cpf_nao_exite: {
    statusCode: 404,
    mensagem: "O CPF fornecido não existe!",
  },
  error_cpf_vazio: {
    statusCode: 422,
    mensagem: "Você deve mandar o CPF do aluno!",
  },
  error_fora_hora_aula: {
    statusCode: 400,
    mensagem: "Fora do horário de aula!",
  },
};
