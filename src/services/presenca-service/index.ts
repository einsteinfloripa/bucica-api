import {
  getAlunoPorCpf,
  getAlunoPorMatricula,
  getPresencaPorMatricula,
  insertPresencaAlunoPorMatricula,
} from "@repositories";
import { errorFactory } from "@utils";
import {
  cpfParser,
  verificarAtraso,
  verificarFinalSemana,
  verificarHorarioAula,
  verificarPresencaFeita,
} from "./utils";

export async function inserirPresencaQR(matriculaId: number) {
  if (verificarHorarioAula()) throw errorFactory("error_fora_hora_aula");
  // if (verificarFinalSemana()) throw errorFactory("error_final_semana");

  if (!matriculaId) throw errorFactory("error_matricula_vazia");

  const aluno = await getAlunoPorMatricula(matriculaId);
  if (!aluno) throw errorFactory("error_matricula_nao_exite");

  const presenca = await getPresencaPorMatricula(matriculaId);
  if (presenca) {
    if (verificarPresencaFeita(presenca)) throw errorFactory("error_presenca_ja_feita");
  }

  const atraso = verificarAtraso();
  insertPresencaAlunoPorMatricula(matriculaId, atraso);

  const mensagemAtraso = "Você chegou atrasado!";
  const mensagemMeiaFalta = "Você recebeu meia falta!";
  const mensagemPresenca = "Presença feita com sucesso!";

  if (atraso === 1) return mensagemAtraso;
  if (atraso === 0.5) return mensagemMeiaFalta;

  return mensagemPresenca;
}

export async function inserirPresencaCPF(cpf: string) {
  if (verificarHorarioAula()) throw errorFactory("error_fora_hora_aula");
  // if (verificarFinalSemana()) throw errorFactory("error_final_semana");

  if (!cpf) throw errorFactory("error_cpf_vazio");

  const aluno = await getAlunoPorCpf(cpfParser(cpf));
  if (!aluno) throw errorFactory("error_cpf_nao_exite");

  const presenca = await getPresencaPorMatricula(aluno.id);
  if (presenca) {
    if (verificarPresencaFeita(presenca)) throw errorFactory("error_presenca_ja_feita");
  }

  insertPresencaAlunoPorMatricula(aluno.id, verificarAtraso());
  return "Presença registrada com sucesso!";
}
