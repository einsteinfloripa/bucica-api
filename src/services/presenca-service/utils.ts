import { isWeekend, setHours, setMinutes, isAfter, isToday } from "date-fns";
import { Presencas } from "@prisma/client";

export function verificarAtraso() {
  const horarioDeAtraso = setHours(setMinutes(new Date(), 15), 18);

  const estaAtrasado = isAfter(new Date(), horarioDeAtraso);

  return estaAtrasado;
}

export function verificarPresencaFeita(presencaData: Presencas) {
  const eHoje = isToday(new Date(presencaData.horario));

  return eHoje;
}

export function verificarFinalSemana() {
  return isWeekend(new Date());
}

export function cpfParser(cpf: string) {
  return cpf.replace(/\D/g, "");
}
