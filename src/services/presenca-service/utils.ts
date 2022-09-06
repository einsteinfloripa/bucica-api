import { Presencas } from "@prisma/client";
import dayjs from "dayjs";
import isToday from "dayjs/plugin/isToday";

dayjs.extend(isToday);

export function verificarAtraso() {
  const horarioDeAtraso = dayjs().hour(18).minute(15);
  const estaAtrasado = dayjs().isBefore(horarioDeAtraso);

  return estaAtrasado;
}

export function verificarPresencaFeita(presencaData: Presencas) {
  const eHoje = dayjs(presencaData.horario).isToday();

  return eHoje;
}
