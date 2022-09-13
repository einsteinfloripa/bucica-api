"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const date_fns_1 = require("date-fns");
const client_1 = require("@prisma/client");
const vitest_1 = require("vitest");
const supertest_1 = __importDefault(require("supertest"));
const app_1 = __importDefault(require("../../src/app"));
(0, vitest_1.describe)("Testes de integração da rota /presenca/qr", () => {
    const prisma = new client_1.PrismaClient();
    const baseUrl = "/presenca/qr";
    (0, vitest_1.beforeEach)(() => __awaiter(void 0, void 0, void 0, function* () {
        yield prisma.$queryRaw `DELETE FROM presencas`;
    }));
    (0, vitest_1.describe)("Registrar Presença (tudo ok)", () => {
        (0, vitest_1.it)("deveria retornar 200", () => __awaiter(void 0, void 0, void 0, function* () {
            const matricula = 22001;
            const response = yield (0, supertest_1.default)(app_1.default).post(`${baseUrl}/${matricula}`);
            (0, vitest_1.expect)(response.status).toBe(200);
            (0, vitest_1.expect)(response.text).toEqual("Presença registrada com sucesso!");
            const presenca = yield prisma.presencas.findMany({ where: { id_aluno: matricula } });
            (0, vitest_1.expect)(presenca[0]).not.toBeUndefined();
        }));
    });
    (0, vitest_1.describe)("Registrar Presença (matrícula não existe)", () => {
        (0, vitest_1.it)("deveria retornar 404", () => __awaiter(void 0, void 0, void 0, function* () {
            const matricula = 224567;
            const response = yield (0, supertest_1.default)(app_1.default).post(`${baseUrl}/${matricula}`);
            (0, vitest_1.expect)(response.status).toBe(404);
            (0, vitest_1.expect)(response.text).toEqual("A matrícula fornecida não existente!");
            const presenca = yield prisma.presencas.findMany({ where: { id_aluno: matricula } });
            (0, vitest_1.expect)(presenca[0]).toBeUndefined();
        }));
    });
    // Vou ter que dar um jeito de mockar o final de semana dps
    if ((0, date_fns_1.isWeekend)(new Date())) {
        (0, vitest_1.describe)("Registrar Presença (final de semana)", () => {
            (0, vitest_1.it)("deveria retornar 400", () => __awaiter(void 0, void 0, void 0, function* () {
                const matricula = 22001;
                const response = yield (0, supertest_1.default)(app_1.default).post(`${baseUrl}/${matricula}`);
                (0, vitest_1.expect)(response.status).toBe(400);
                (0, vitest_1.expect)(response.text).toEqual("Não é possível registrar presença no final de semana!");
                const presenca = yield prisma.presencas.findMany({ where: { id_aluno: matricula } });
                (0, vitest_1.expect)(presenca[0]).toBeUndefined();
            }));
        });
    }
    (0, vitest_1.describe)("Registrar Presença (presença já feita)", () => {
        (0, vitest_1.it)("deveria retornar 400", () => __awaiter(void 0, void 0, void 0, function* () {
            yield prisma.presencas.create({ data: { id_aluno: 22001, atrasado: false } });
            const matricula = 22001;
            const response = yield (0, supertest_1.default)(app_1.default).post(`${baseUrl}/${matricula}`);
            (0, vitest_1.expect)(response.status).toBe(400);
            (0, vitest_1.expect)(response.text).toEqual("Já foi feito a presença do aluno hoje!");
            const presenca = yield prisma.presencas.findMany({ where: { id_aluno: matricula } });
            (0, vitest_1.expect)(presenca.length).toBe(1);
        }));
    });
    (0, vitest_1.afterAll)(() => prisma.$disconnect());
});
(0, vitest_1.describe)("Testes de integração da rota /presenca/cpf", () => {
    const prisma = new client_1.PrismaClient();
    const baseUrl = "/presenca/cpf";
    (0, vitest_1.beforeEach)(() => __awaiter(void 0, void 0, void 0, function* () {
        yield prisma.$queryRaw `DELETE FROM presencas`;
    }));
    (0, vitest_1.describe)("Registrar Presença (tudo ok)", () => {
        (0, vitest_1.it)("deveria retornar 200", () => __awaiter(void 0, void 0, void 0, function* () {
            const cpf = "11818039931";
            const response = yield (0, supertest_1.default)(app_1.default).post(`${baseUrl}/${cpf}`);
            (0, vitest_1.expect)(response.status).toBe(200);
            (0, vitest_1.expect)(response.text).toEqual("Presença registrada com sucesso!");
            const aluno = yield prisma.alunos.findFirst({ where: { cpf } });
            const presenca = yield prisma.presencas.findMany({ where: { id_aluno: aluno.id } });
            (0, vitest_1.expect)(presenca[0]).not.toBeUndefined();
        }));
    });
    (0, vitest_1.describe)("Registrar Presença (matrícula não existe)", () => {
        (0, vitest_1.it)("deveria retornar 404", () => __awaiter(void 0, void 0, void 0, function* () {
            const cpf = "118180399312";
            const response = yield (0, supertest_1.default)(app_1.default).post(`${baseUrl}/${cpf}`);
            (0, vitest_1.expect)(response.status).toBe(404);
            (0, vitest_1.expect)(response.text).toEqual("O CPF fornecido não existe!");
            const aluno = yield prisma.alunos.findFirst({ where: { cpf } });
            const presenca = yield prisma.presencas.findMany({ where: { id_aluno: aluno === null || aluno === void 0 ? void 0 : aluno.id } });
            (0, vitest_1.expect)(presenca[0]).toBeUndefined();
        }));
    });
    // Vou ter que dar um jeito de mockar o final de semana dps
    if ((0, date_fns_1.isWeekend)(new Date())) {
        (0, vitest_1.describe)("Registrar Presença (final de semana)", () => {
            (0, vitest_1.it)("deveria retornar 400", () => __awaiter(void 0, void 0, void 0, function* () {
                const cpf = "11818039931";
                const response = yield (0, supertest_1.default)(app_1.default).post(`${baseUrl}/${cpf}`);
                (0, vitest_1.expect)(response.status).toBe(400);
                (0, vitest_1.expect)(response.text).toEqual("Não é possível registrar presença no final de semana!");
                const aluno = yield prisma.alunos.findFirst({ where: { cpf } });
                const presenca = yield prisma.presencas.findMany({ where: { id_aluno: aluno.id } });
                (0, vitest_1.expect)(presenca[0]).toBeUndefined();
            }));
        });
    }
    (0, vitest_1.describe)("Registrar Presença (presença já feita)", () => {
        (0, vitest_1.it)("deveria retornar 400", () => __awaiter(void 0, void 0, void 0, function* () {
            const cpf = "11818039931";
            const aluno = yield prisma.alunos.findFirst({ where: { cpf } });
            yield prisma.presencas.create({ data: { id_aluno: aluno.id, atrasado: false } });
            const response = yield (0, supertest_1.default)(app_1.default).post(`${baseUrl}/${cpf}`);
            (0, vitest_1.expect)(response.status).toBe(400);
            (0, vitest_1.expect)(response.text).toEqual("Já foi feito a presença do aluno hoje!");
            const presenca = yield prisma.presencas.findMany({ where: { id_aluno: aluno.id } });
            (0, vitest_1.expect)(presenca.length).toBe(1);
        }));
    });
    (0, vitest_1.afterAll)(() => prisma.$disconnect());
});
