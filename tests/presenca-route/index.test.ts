import { isWeekend } from "date-fns";
import { Alunos, PrismaClient } from "@prisma/client";
import { afterAll, afterEach, beforeEach, describe, expect, it as test, vi } from "vitest";
import supertest from "supertest";

import app from "../../src/app";

describe("Testes de integração da rota /presenca/qr", () => {
  const prisma = new PrismaClient();
  const baseUrl = "/presenca/qr";

  beforeEach(async () => {
    await prisma.$queryRaw`DELETE FROM presencas`;
  });

  afterEach(() => {
    vi.clearAllMocks();
    vi.resetAllMocks();
  });

  des
  test("deveria retornar 400", async () => {
    vi.mock("../../src/services/presenca-service/utils", () => ({
      verificarHorarioAula: vi.fn(() => true),
    }));

    const matricula = 22001;
    const response = await supertest(app).post(`${baseUrl}/${matricula}`);

    expect(response.status).toBe(400);
    expect(response.text).toEqual("Fora do horário de aula!");

    const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
    expect(presenca.length).toBe(0);
  });

  // Vou ter que dar um jeito de mockar o final de semana dps
  // describe("Registrar Presença (final de semana)", () => {
  //   it("deveria retornar 400", async () => {
  //     const matricula = 22001;
  //     const response = await supertest(app).post(`${baseUrl}/${matricula}`);

  //     expect(response.status).toBe(400);
  //     expect(response.text).toEqual("Não é possível registrar presença no final de semana!");

  //     const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
  //     expect(presenca[0]).toBeUndefined();
  //   });
  // });

  test("deveria retornar 404", async () => {
    vi.mock("../../src/services/presenca-service/utils", () => ({
      verificarHorarioAula: vi.fn(() => false),
    }));
    const matricula = 224567;
    const response = await supertest(app).post(`${baseUrl}/${matricula}`);

    expect(response.status).toBe(404);
    expect(response.text).toEqual("A matrícula fornecida não existente!");

    const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
    expect(presenca[0]).toBeUndefined();
  });

  test("deveria retornar 400", async () => {
    vi.mock("../../src/services/presenca-service/utils", () => ({
      verificarHorarioAula: vi.fn(() => false),
    }));
    await prisma.presencas.create({ data: { id_aluno: 22001, atrasado: 0 } });

    const matricula = 22001;
    const response = await supertest(app).post(`${baseUrl}/${matricula}`);

    expect(response.status).toBe(400);
    expect(response.text).toEqual("Já foi feito a presença do aluno hoje!");

    const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
    expect(presenca.length).toBe(1);
  });

  test("deveria retornar 200", async () => {
    vi.mock("../../src/services/presenca-service/utils", () => ({
      verificarHorarioAula: vi.fn(() => false),
      verificarAtraso: vi.fn(() => 1),
    }));
    const matricula = 22001;
    const response = await supertest(app).post(`${baseUrl}/${matricula}`);

    expect(response.status).toBe(200);
    expect(response.text).toEqual("Você chegou atrasado!");

    const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
    expect(presenca[0]).not.toBeUndefined();
    expect(presenca[0].atrasado).toBe(1);
  });

  test("deveria retornar 200", async () => {
    vi.mock("../../src/services/presenca-service/utils", () => ({
      verificarHorarioAula: vi.fn(() => false),
      verificarAtraso: vi.fn(() => 0.5),
    }));
    const matricula = 22001;
    const response = await supertest(app).post(`${baseUrl}/${matricula}`);

    expect(response.status).toBe(200);
    expect(response.text).toEqual("Você recebeu meia falta!");

    const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
    expect(presenca[0]).not.toBeUndefined();
    expect(presenca[0].atrasado).toBe(0.5);
  });

  test("deveria retornar 200", async () => {
    vi.mock("../../src/services/presenca-service/utils", () => ({
      verificarHorarioAula: vi.fn(() => false),
      verificarAtraso: vi.fn(() => 0),
    }));
    const matricula = 22001;
    const response = await supertest(app).post(`${baseUrl}/${matricula}`);

    expect(response.status).toBe(200);
    expect(response.text).toEqual("Presença registrada com sucesso!");

    const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
    expect(presenca[0]).not.toBeUndefined();
    expect(presenca[0].atrasado).toBe(0);
  });

  afterAll(() => prisma.$disconnect());
});

// describe("Testes de integração da rota /presenca/cpf", () => {
//   const prisma = new PrismaClient();
//   const baseUrl = "/presenca/cpf";

//   beforeEach(async () => {
//     await prisma.$queryRaw`DELETE FROM presencas`;
//   });

//   describe("Registrar Presença (tudo ok)", () => {
//     it("deveria retornar 200", async () => {
//       const cpf = "11818039931";
//       const response = await supertest(app).post(`${baseUrl}/${cpf}`);

//       expect(response.status).toBe(200);
//       expect(response.text).toEqual("Presença registrada com sucesso!");

//       const aluno = (await prisma.alunos.findFirst({ where: { cpf } })) as Alunos;

//       const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno.id } });
//       expect(presenca[0]).not.toBeUndefined();
//     });
//   });

//   describe("Registrar Presença (matrícula não existe)", () => {
//     it("deveria retornar 404", async () => {
//       const cpf = "118180399312";
//       const response = await supertest(app).post(`${baseUrl}/${cpf}`);

//       expect(response.status).toBe(404);
//       expect(response.text).toEqual("O CPF fornecido não existe!");

//       const aluno = await prisma.alunos.findFirst({ where: { cpf } });
//       const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno?.id } });
//       expect(presenca[0]).toBeUndefined();
//     });
//   });

//   describe("Registrar Presença (presença já feita)", () => {
//     it("deveria retornar 400", async () => {
//       const cpf = "11818039931";
//       const aluno = (await prisma.alunos.findFirst({ where: { cpf } })) as Alunos;
//       await prisma.presencas.create({ data: { id_aluno: aluno.id, atrasado: 0 } });

//       const response = await supertest(app).post(`${baseUrl}/${cpf}`);

//       expect(response.status).toBe(400);
//       expect(response.text).toEqual("Já foi feito a presença do aluno hoje!");

//       const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno.id } });
//       expect(presenca.length).toBe(1);
//     });
//   });

//   afterAll(() => prisma.$disconnect());
// });
