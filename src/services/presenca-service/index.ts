import { getAlunoPorMatricula, getPresencaPorMatricula, insertPresencaAlunoPorMatricula } from "@repositories";
import { errorFactory } from "@utils";
import { verificarAtraso, verificarFinalSemana, verificarPresencaFeita } from "./utils";

export async function inserirPresenca(matriculaId: number) {
  if (!matriculaId) throw errorFactory("error_matricula_vazia");

  const aluno = await getAlunoPorMatricula(matriculaId);
  if (!aluno) throw errorFactory("error_matricua_nao_exite");

  const presenca = await getPresencaPorMatricula(matriculaId);
  if (verificarFinalSemana(presenca)) throw errorFactory("error_final_semana");
  if (verificarPresencaFeita(presenca)) throw errorFactory("error_presenca_ja_feita");

  await insertPresencaAlunoPorMatricula(matriculaId, verificarAtraso());
  return "Presença feita com sucesso!";
}
