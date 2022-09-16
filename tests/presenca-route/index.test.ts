import { Alunos, PrismaClient } from "@prisma/client";
import { afterAll, afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import supertest from "supertest";

import app from "../../src/app";
import * as utils from "../../src/services/presenca-service/utils";
import { alunoFakeData } from "./factories";

describe("Testes de integração da rota /presenca/qr", async () => {
  const prisma = new PrismaClient();
  const baseUrl = "/presenca/qr";

  await prisma.alunos.create({
    data: alunoFakeData,
  });

  beforeEach(async () => {
    await prisma.$executeRaw`DELETE FROM presencas`;
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe("Registar presença QR (fora horario de aula)", () => {
    test("deveria retornar 400", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(true);

      const matricula = 22001;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(400);
      expect(response.text).toEqual("Fora do horário de aula!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
      expect(presenca.length).toBe(0);
    });
  });

  describe("Registrar presença QR (matricula nao existe))", () => {
    test("deveria retornar 404", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);

      const matricula = 224567;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(404);
      expect(response.text).toEqual("A matrícula fornecida não existente!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
      expect(presenca[0]).toBeUndefined();
    });
  });

  describe("Registra presença QR (presença ja feita))", () => {
    test("deveria retornar 400", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);

      await prisma.presencas.create({ data: { id_aluno: 22001, atrasado: 0 } });

      const matricula = 22001;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(400);
      expect(response.text).toEqual("Já foi feito a presença do aluno hoje!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
      expect(presenca.length).toBe(1);
    });
  });

  describe("Registrar presença QR (falta)", () => {
    test("deveria retornar 200", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);
      vi.spyOn(utils, "verificarAtraso").mockReturnValue(1);

      const matricula = 22001;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Você chegou atrasado!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });

      expect(presenca[0]).not.toBeUndefined();
      expect(presenca[0].atrasado).toBe(1);
    });
  });

  describe("Registrar presença QR (meia falta)", () => {
    test("deveria retornar 200", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);
      vi.spyOn(utils, "verificarAtraso").mockReturnValue(0.5);

      const matricula = 22001;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Você recebeu meia falta!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });

      expect(presenca[0]).not.toBeUndefined();
      expect(presenca[0].atrasado).toBe(0.5);
    });
  });

  describe("Registrar presença QR (tudo ok)", () => {
    test("deveria retornar 200", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);
      vi.spyOn(utils, "verificarAtraso").mockReturnValue(0);

      const matricula = 22001;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Presença feita com sucesso!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });

      expect(presenca[0]).not.toBeUndefined();
      expect(presenca[0].atrasado).toBe(0);
    });
  });

  afterAll(() => prisma.$disconnect());
});

describe("Testes de integração da rota /presenca/cpf", async () => {
  const prisma = new PrismaClient();
  const baseUrl = "/presenca/cpf";

  beforeEach(async () => {
    await prisma.$executeRaw`DELETE FROM presencas`;
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe("Registar presença CPF (fora horario de aula)", () => {
    test("deveria retornar 400", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(true);

      const cpf = "118180399312";
      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(400);
      expect(response.text).toEqual("Fora do horário de aula!");

      const aluno = await prisma.alunos.findFirst({ where: { cpf } });
      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno?.id } });

      expect(presenca.length).toBe(0);
    });
  });

  describe("Registrar Presença CPF (matrícula não existe)", () => {
    test("deveria retornar 404", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);

      const cpf = "118180399312";
      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(404);
      expect(response.text).toEqual("O CPF fornecido não existe!");

      const aluno = await prisma.alunos.findFirst({ where: { cpf } });
      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno?.id } });

      expect(presenca[0]).toBeUndefined();
    });
  });

  describe("Registrar Presença CPF (presença já feita)", () => {
    test("deveria retornar 400", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);

      const cpf = "11818039931";
      const aluno = (await prisma.alunos.findFirst({ where: { cpf } })) as Alunos;

      await prisma.presencas.create({ data: { id_aluno: aluno?.id, atrasado: 0 } });
      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(400);
      expect(response.text).toEqual("Já foi feito a presença do aluno hoje!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno?.id } });
      expect(presenca.length).toBe(1);
    });
  });

  describe("Registrar Presença CPF (falta)", () => {
    test("deveria retornar 200", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);
      vi.spyOn(utils, "verificarAtraso").mockReturnValue(1);

      const cpf = "11818039931";
      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Você chegou atrasado!");

      const aluno = (await prisma.alunos.findFirst({ where: { cpf } })) as Alunos;
      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno.id } });

      expect(presenca[0]).not.toBeUndefined();
      expect(presenca[0].atrasado).toBe(1);
    });
  });

  describe("Registrar Presença CPF (meia falta)", () => {
    test("deveria retornar 200", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);
      vi.spyOn(utils, "verificarAtraso").mockReturnValue(0.5);

      const cpf = "11818039931";
      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Você recebeu meia falta!");

      const aluno = (await prisma.alunos.findFirst({ where: { cpf } })) as Alunos;
      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno.id } });

      expect(presenca[0]).not.toBeUndefined();
      expect(presenca[0].atrasado).toBe(0.5);
    });
  });

  describe("Registrar Presença CPF (tudo ok)", () => {
    test("deveria retornar 200", async () => {
      vi.spyOn(utils, "verificarHorarioAula").mockReturnValue(false);
      vi.spyOn(utils, "verificarAtraso").mockReturnValue(0);

      const cpf = "11818039931";
      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Presença feita com sucesso!");

      const aluno = (await prisma.alunos.findFirst({ where: { cpf } })) as Alunos;
      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno.id } });

      expect(presenca[0]).not.toBeUndefined();
      expect(presenca[0].atrasado).toBe(0);
    });
  });

  afterAll(() => prisma.$disconnect());
});
