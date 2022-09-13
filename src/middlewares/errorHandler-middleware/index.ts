/* eslint-disable @typescript-eslint/no-unused-vars */
import { NextFunction, Request, Response } from "express";

export interface Error {
  statusCode: number;
  mensagem: string;
}

export function errorHandlerMiddleware(err: Error, req: Request, res: Response, next: NextFunction) {
  return res.status(err.statusCode).send(err.mensagem);
}
