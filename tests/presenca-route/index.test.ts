import { PrismaClient } from "@prisma/client";
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";
import supertest from "supertest";
import dayjs from "dayjs";
import weekday from "dayjs/plugin/weekday";

import app from "../../src/app";

dayjs.extend(weekday);

const prisma = new PrismaClient();

const isWeekend = dayjs().weekday() === 0 || dayjs().weekday() === 7;

describe("Testes de integração da rota /presenca", () => {
  beforeEach(async () => {
    await prisma.$queryRaw`DELETE FROM presencas`;
  });

  describe("Registrar Presença (tudo ok)", () => {
    it("deveria retornar 200", async () => {
      const matricula = 22001;
      const response = await supertest(app).post(`/presenca/${matricula}`);

      expect(response.status).toBe(200);
      expect(response.text).toEqual("Presença registrada com sucesso!");
    });
  });

  describe("Registrar Presença (matrícula não existe)", () => {
    it("deveria retornar 404", async () => {
      const response = await supertest(app).post("/presenca/224321");

      expect(response.status).toBe(404);
      expect(response.text).toEqual("A matrícula fornecida não existente!");
    });
  });

  if (isWeekend) {
    describe("Registrar Presença (final de semana)", () => {
      it("deveria retornar 400", async () => {
        const response = await supertest(app).post("/presenca/22001");

        expect(response.status).toBe(400);
        expect(response.text).toEqual("Não é possível registrar presença no final de semana!");
      });
    });
  }

  describe("Registrar Presença (presença já feita)", () => {
    it("deveria retornar 400", async () => {
      await prisma.presencas.create({ data: { id_aluno: 22001, atrasado: false } });
      const response = await supertest(app).post("/presenca/22001");

      expect(response.status).toBe(400);
      expect(response.text).toEqual("Já foi feito a presença do aluno hoje!");
    });
  });
});
