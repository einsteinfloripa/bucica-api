import dayjs from "dayjs";
import isToday from "dayjs/plugin/isToday";
import weekday from "dayjs/plugin/weekday";
import { Presencas } from "@prisma/client";

dayjs.extend(isToday);
dayjs.extend(weekday);

export function verificarAtraso() {
  const horarioDeAtraso = dayjs().hour(18).minute(15);
  const estaAtrasado = dayjs().isBefore(horarioDeAtraso);

  return estaAtrasado;
}

export function verificarPresencaFeita(presencaData: Presencas) {
  const eHoje = dayjs(presencaData.horario).isToday();

  return eHoje;
}

export function verificarFinalSemana(presencaData: Presencas) {
  const weekday = dayjs(presencaData.horario).weekday();

  return weekday === 0 || weekday === 7; //0 é igual domingo e 7 igual a sábado
}
