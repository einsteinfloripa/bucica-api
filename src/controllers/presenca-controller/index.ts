import { Request, Response } from "express";

import { inserirPresenca } from "@services";

interface PresencaParams {
  matriculaId: number;
}

export async function postPresencaController(req: Request<PresencaParams>, res: Response) {
  const { matriculaId } = req.params;
  const returnService = await inserirPresenca(matriculaId);

  res.send(returnService);
}
