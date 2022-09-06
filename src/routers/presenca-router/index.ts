import { Router } from "express";

import { postPresencaController } from "@controllers";

export const presencaRouter = Router();

presencaRouter.post("/:matriculaId", postPresencaController);
