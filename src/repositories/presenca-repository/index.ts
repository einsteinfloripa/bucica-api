import { prisma } from "@db";

export async function getAlunoPorMatricula(matriculaId: number) {
  const aluno = await prisma.alunos.findUnique({ where: { id: +matriculaId } });

  return aluno;
}

export async function insertPresencaAlunoPorMatricula(matriculaId: number, atrasado: boolean) {
  return await prisma.presencas.create({ data: { id_aluno: +matriculaId, atrasado: atrasado } });
}

export async function getPresencaPorMatricula(matriculaId: number) {
  return await prisma.presencas.findFirst({ where: { id_aluno: +matriculaId }, orderBy: { horario: "desc" } });
}
