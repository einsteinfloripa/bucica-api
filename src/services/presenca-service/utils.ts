import { isWeekend, setHours, setMinutes, isAfter, isToday, isBefore } from "date-fns";
import { Presencas } from "@prisma/client";

export function verificarAtraso() {
  const estaEmMeiaFalta = verificarMeiaFalta();

  const valorMeiaFalta = estaEmMeiaFalta ? 0.5 : 0;
  const valorFaltaCompleta = estaEmMeiaFalta ? 0 : 1;

  return valorMeiaFalta + valorFaltaCompleta;
}

export function verificarHorarioAula() {
  const inicioHorarioDeAula = setHours(setMinutes(new Date(), 50), 20);
  const fimHorarioDeAula = setHours(setMinutes(new Date(), 50), 21);

  const estaAntesDoHoraDaAula = isBefore(new Date(), inicioHorarioDeAula);
  const estaDepoisDoHoraDaAula = isAfter(new Date(), fimHorarioDeAula);

  return estaAntesDoHoraDaAula || estaDepoisDoHoraDaAula;
}

function verificarMeiaFalta() {
  const iniciohorarioDeMeiaFalta = setHours(setMinutes(new Date(), 15), 21);
  const finalhorarioDeMeiaFalta = setHours(setMinutes(new Date(), 50), 21);

  const estaAntesDoHoraDaMeiaFalta = isBefore(new Date(), finalhorarioDeMeiaFalta);
  const estaDepoisDoHoraDaMeiaFalta = isAfter(new Date(), iniciohorarioDeMeiaFalta);

  return estaAntesDoHoraDaMeiaFalta && estaDepoisDoHoraDaMeiaFalta;
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


