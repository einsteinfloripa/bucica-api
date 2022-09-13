import {
  getAlunoPorCpf,
  getAlunoPorMatricula,
  getPresencaPorMatricula,
  insertPresencaAlunoPorMatricula,
} from "@repositories";
import { errorFactory } from "@utils";
import { cpfParser, verificarAtraso, verificarFinalSemana, verificarPresencaFeita } from "./utils";

export async function inserirPresencaQR(matriculaId: number) {
  if (!matriculaId) throw errorFactory("error_matricula_vazia");

  const aluno = await getAlunoPorMatricula(matriculaId);
  if (!aluno) throw errorFactory("error_matricula_nao_exite");

  if (verificarFinalSemana()) throw errorFactory("error_final_semana");

  const presenca = await getPresencaPorMatricula(matriculaId);
  if (presenca) {
    if (verificarPresencaFeita(presenca)) throw errorFactory("error_presenca_ja_feita");
  }

  insertPresencaAlunoPorMatricula(matriculaId, verificarAtraso());

  return "Presença registrada com sucesso!";
}

export async function inserirPresencaCPF(cpf: string) {
  const aluno = await getAlunoPorCpf(cpfParser(cpf));
  if (!aluno) throw errorFactory("error_cpf_nao_exite");

  if (verificarFinalSemana()) throw errorFactory("error_final_semana");

  const presenca = await getPresencaPorMatricula(aluno.id);
  if (presenca) {
    if (verificarPresencaFeita(presenca)) throw errorFactory("error_presenca_ja_feita");
  }

  insertPresencaAlunoPorMatricula(aluno.id, verificarAtraso());
  return "Presença registrada com sucesso!";
}
