import { isWeekend } from "date-fns";
import { PrismaClient } from "@prisma/client";
import { afterAll, beforeEach, describe, expect, it } from "vitest";
import supertest from "supertest";

import app from "../../src/app";

describe("Testes de integração da rota /presenca/qr", () => {
  const prisma = new PrismaClient();
  const baseUrl = "/presenca/qr";
  beforeEach(async () => {
    await prisma.$queryRaw`DELETE FROM presencas`;
  });

  describe("Registrar Presença (tudo ok)", () => {
    it("deveria retornar 200", async () => {
      const matricula = 22001;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Presença registrada com sucesso!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
      expect(presenca[0]).not.toBeUndefined();
    });
  });

  describe("Registrar Presença (matrícula não existe)", () => {
    it("deveria retornar 404", async () => {
      const matricula = 224567;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(404);
      expect(response.text).toEqual("A matrícula fornecida não existente!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
      expect(presenca[0]).toBeUndefined();
    });
  });

  // Vou ter que dar um jeito de mockar o final de semana dps
  if (isWeekend(new Date())) {
    describe("Registrar Presença (final de semana)", () => {
      it("deveria retornar 400", async () => {
        const matricula = 22001;
        const response = await supertest(app).post(`${baseUrl}/${matricula}`);

        expect(response.status).toBe(400);
        expect(response.text).toEqual("Não é possível registrar presença no final de semana!");

        const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
        expect(presenca[0]).toBeUndefined();
      });
    });
  }

  describe("Registrar Presença (presença já feita)", () => {
    it("deveria retornar 400", async () => {
      await prisma.presencas.create({ data: { id_aluno: 22001, atrasado: false } });

      const matricula = 22001;
      const response = await supertest(app).post(`${baseUrl}/${matricula}`);

      expect(response.status).toBe(400);
      expect(response.text).toEqual("Já foi feito a presença do aluno hoje!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: matricula } });
      expect(presenca.length).toBe(1);
    });
  });

  afterAll(() => prisma.$disconnect());
});

describe("Testes de integração da rota /presenca/cpf", () => {
  const prisma = new PrismaClient();
  const baseUrl = "/presenca/cpf";

  beforeEach(async () => {
    await prisma.$queryRaw`DELETE FROM presencas`;
  });

  describe("Registrar Presença (tudo ok)", () => {
    it("deveria retornar 200", async () => {
      const cpf = "11818039931";
      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Presença registrada com sucesso!");

      const aluno = await prisma.alunos.findFirst({ where: { cpf } });

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno.id } });
      expect(presenca[0]).not.toBeUndefined();
    });
  });

  describe("Registrar Presença (matrícula não existe)", () => {
    it("deveria retornar 404", async () => {
      const cpf = "118180399312";
      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(404);
      expect(response.text).toEqual("O CPF fornecido não existe!");

      const aluno = await prisma.alunos.findFirst({ where: { cpf } });
      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno?.id } });
      expect(presenca[0]).toBeUndefined();
    });
  });

  // Vou ter que dar um jeito de mockar o final de semana dps
  if (isWeekend(new Date())) {
    describe("Registrar Presença (final de semana)", () => {
      it("deveria retornar 400", async () => {
        const cpf = "11818039931";
        const response = await supertest(app).post(`${baseUrl}/${cpf}`);

        expect(response.status).toBe(400);
        expect(response.text).toEqual("Não é possível registrar presença no final de semana!");

        const aluno = await prisma.alunos.findFirst({ where: { cpf } });
        const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno.id } });
        expect(presenca[0]).toBeUndefined();
      });
    });
  }

  describe("Registrar Presença (presença já feita)", () => {
    it("deveria retornar 400", async () => {
      const cpf = "11818039931";
      const aluno = await prisma.alunos.findFirst({ where: { cpf } });
      await prisma.presencas.create({ data: { id_aluno: aluno.id, atrasado: false } });

      const response = await supertest(app).post(`${baseUrl}/${cpf}`);

      expect(response.status).toBe(400);
      expect(response.text).toEqual("Já foi feito a presença do aluno hoje!");

      const presenca = await prisma.presencas.findMany({ where: { id_aluno: aluno.id } });
      expect(presenca.length).toBe(1);
    });
  });

  afterAll(() => prisma.$disconnect());
});
