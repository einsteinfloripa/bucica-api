import { Router } from "express";
import { postCPFPresencaController, postQRPresencaController } from "@controllers";

export const presencaRouter = Router();

presencaRouter.post("/qr/:matriculaId", postQRPresencaController);
presencaRouter.post("/cpf/:cpf", postCPFPresencaController);
