import { getAlunoPorMatricula, getPresencaPorMatricula, insertPresencaAlunoPorMatricula } from "@repositories";
import { verificarAtraso, verificarPresencaFeita } from "./utils";

export async function inserirPresenca(matriculaId: number) {
  if (!matriculaId) return "Você deve mandar a matrícula do aluno!";

  const aluno = await getAlunoPorMatricula(matriculaId);
  if (!aluno) return "A matricula fornecida não existente!";

  const presenca = await getPresencaPorMatricula(matriculaId);
  if (verificarPresencaFeita(presenca)) return "Já foi feito a presenca do aluno hoje!";

  await insertPresencaAlunoPorMatricula(matriculaId, verificarAtraso());
  return "Presença feita com sucesso!";
}
