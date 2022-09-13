import { Request, Response } from "express";
import { inserirPresencaCPF, inserirPresencaQR } from "@services";

interface PresencaQRParams {
  matriculaId: number;
}

interface PresencaCPFParams {
  cpf: string;
}

export async function postQRPresencaController(req: Request<PresencaQRParams>, res: Response) {
  const { matriculaId } = req.params;
  const returnService = await inserirPresencaQR(matriculaId);

  res.send(returnService);
}

export async function postCPFPresencaController(req: Request<PresencaCPFParams>, res: Response) {
  const { cpf } = req.params;
  const returnService = await inserirPresencaCPF(cpf);

  res.send(returnService);
}
