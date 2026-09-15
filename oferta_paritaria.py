"""Escenarios de comparacion entre oferta salarial anterior y ultima."""

from __future__ import annotations

from collections import OrderedDict

from configuracion import (
    MONTO_FOID_CARGO_SIMPLE,
    MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
    TASA_FUNCION_DOCENTE,
    TASA_TRANSFORMACION_EDUCATIVA,
    VALORES_INDICE_REFERENCIA,
)
from remunerativos import calcular_asignacion_hora_catedra
from salario import calcular_salario


VALOR_INDICE_ACTUAL = VALORES_INDICE_REFERENCIA["Julio 2026 Decreto 1059/26"]

TASA_FUNCION_DOCENTE_ANTERIOR = 2.39
TASA_FUNCION_DOCENTE_ULTIMA_SEPTIEMBRE = 2.55
TASA_FUNCION_DOCENTE_ULTIMA_OCTUBRE = 2.65
TASA_FUNCION_DOCENTE_ULTIMA_NOVIEMBRE = 2.70
TASA_FUNCION_DOCENTE_ULTIMA_ENERO = 2.85

MONTO_FOID_ANTERIOR = 100000.00
MONTO_FOID_ULTIMA_INICIAL = MONTO_FOID_CARGO_SIMPLE
MONTO_FOID_ULTIMA_NOVIEMBRE = 70000.00
MONTO_FOID_ULTIMA_ENERO = 90000.00

MESES_COMPARACION = [
    {
        "clave": "septiembre_2026",
        "mes_haber": "Septiembre 2026",
        "mes_cobro": "Octubre 2026",
    },
    {
        "clave": "octubre_2026",
        "mes_haber": "Octubre 2026",
        "mes_cobro": "Noviembre 2026",
    },
    {
        "clave": "noviembre_2026",
        "mes_haber": "Noviembre 2026",
        "mes_cobro": "Diciembre 2026",
    },
    {
        "clave": "diciembre_2026",
        "mes_haber": "Diciembre 2026",
        "mes_cobro": "Enero 2027",
    },
    {
        "clave": "enero_2027",
        "mes_haber": "Enero 2027",
        "mes_cobro": "Febrero 2027",
    },
]

ESCENARIO_ACTUAL = {
    "clave": "actual_agosto_2026",
    "nombre": "Actual cobrado",
    "subtitulo": "Haberes agosto 2026",
    "propuesta": "actual",
    "valor_indice": VALOR_INDICE_ACTUAL,
    "tasa_funcion_docente": TASA_FUNCION_DOCENTE,
    "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
    "monto_foid": MONTO_FOID_CARGO_SIMPLE,
    "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
    "asignacion_412_extra": False,
    "detalle": "Base actual cobrada por agosto con los parametros vigentes.",
}

PROPUESTA_ANTERIOR = OrderedDict(
    [
        (
            "septiembre_2026",
            {
                "clave": "anterior_septiembre_2026",
                "nombre": "Propuesta anterior",
                "subtitulo": "Septiembre 2026",
                "propuesta": "anterior",
                "valor_indice": VALOR_INDICE_ACTUAL * 1.01,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ANTERIOR,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ANTERIOR,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Acta anterior: Funcion Docente 239%, valor indice +1% y FOID $100.000.",
            },
        ),
        (
            "octubre_2026",
            {
                "clave": "anterior_octubre_2026",
                "nombre": "Propuesta anterior",
                "subtitulo": "Octubre 2026",
                "propuesta": "anterior",
                "valor_indice": VALOR_INDICE_ACTUAL * 1.01 * 1.01,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ANTERIOR,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ANTERIOR,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Acta anterior: segundo tramo acumulado de +1% al valor indice.",
            },
        ),
        (
            "noviembre_2026",
            {
                "clave": "anterior_noviembre_2026",
                "nombre": "Propuesta anterior",
                "subtitulo": "Noviembre 2026",
                "propuesta": "anterior",
                "valor_indice": VALOR_INDICE_ACTUAL * 1.01 * 1.01 * 1.01,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ANTERIOR,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ANTERIOR,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Acta anterior: tercer tramo acumulado de +1% al valor indice.",
            },
        ),
        (
            "diciembre_2026",
            {
                "clave": "anterior_diciembre_2026",
                "nombre": "Propuesta anterior",
                "subtitulo": "Diciembre 2026",
                "propuesta": "anterior",
                "valor_indice": VALOR_INDICE_ACTUAL * 1.01 * 1.01 * 1.01,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ANTERIOR,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ANTERIOR,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Acta anterior: sin nuevo tramo para diciembre; se mantiene el valor acumulado de noviembre.",
            },
        ),
        (
            "enero_2027",
            {
                "clave": "anterior_enero_2027",
                "nombre": "Propuesta anterior",
                "subtitulo": "Enero 2027",
                "propuesta": "anterior",
                "valor_indice": VALOR_INDICE_ACTUAL * 1.01 * 1.01 * 1.01,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ANTERIOR,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ANTERIOR,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": True,
                "detalle": "Acta anterior: suma una asignacion equivalente al concepto 412 en enero.",
            },
        ),
    ]
)

PROPUESTA_ULTIMA = OrderedDict(
    [
        (
            "septiembre_2026",
            {
                "clave": "ultima_septiembre_2026",
                "nombre": "Ultima propuesta",
                "subtitulo": "Septiembre 2026",
                "propuesta": "ultima",
                "valor_indice": VALOR_INDICE_ACTUAL,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ULTIMA_SEPTIEMBRE,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ULTIMA_INICIAL,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Ultima acta: Funcion Docente 255%. El FOID sigue en $56.000.",
            },
        ),
        (
            "octubre_2026",
            {
                "clave": "ultima_octubre_2026",
                "nombre": "Ultima propuesta",
                "subtitulo": "Octubre 2026",
                "propuesta": "ultima",
                "valor_indice": VALOR_INDICE_ACTUAL,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ULTIMA_OCTUBRE,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ULTIMA_INICIAL,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Ultima acta: Funcion Docente 265%.",
            },
        ),
        (
            "noviembre_2026",
            {
                "clave": "ultima_noviembre_2026",
                "nombre": "Ultima propuesta",
                "subtitulo": "Noviembre 2026",
                "propuesta": "ultima",
                "valor_indice": VALOR_INDICE_ACTUAL,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ULTIMA_NOVIEMBRE,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ULTIMA_NOVIEMBRE,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Ultima acta: Funcion Docente 270% y FOID $70.000.",
            },
        ),
        (
            "diciembre_2026",
            {
                "clave": "ultima_diciembre_2026",
                "nombre": "Ultima propuesta",
                "subtitulo": "Diciembre 2026",
                "propuesta": "ultima",
                "valor_indice": VALOR_INDICE_ACTUAL,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ULTIMA_NOVIEMBRE,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ULTIMA_NOVIEMBRE,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Ultima acta: sin nuevo tramo para diciembre; se mantiene Funcion Docente 270% y FOID $70.000.",
            },
        ),
        (
            "enero_2027",
            {
                "clave": "ultima_enero_2027",
                "nombre": "Ultima propuesta",
                "subtitulo": "Enero 2027",
                "propuesta": "ultima",
                "valor_indice": VALOR_INDICE_ACTUAL,
                "tasa_funcion_docente": TASA_FUNCION_DOCENTE_ULTIMA_ENERO,
                "tasa_transformacion_educativa": TASA_TRANSFORMACION_EDUCATIVA,
                "monto_foid": MONTO_FOID_ULTIMA_ENERO,
                "monto_material": MONTO_MATERIAL_DIDACTICO_CARGO_SIMPLE,
                "asignacion_412_extra": False,
                "detalle": "Ultima acta: Funcion Docente 285% y FOID $90.000.",
            },
        ),
    ]
)

CRONOGRAMA_RESTITUCION_DESCUENTOS = [
    {"Haber con descuento": "Enero 2026", "Haber de reintegro": "Septiembre 2026"},
    {"Haber con descuento": "Febrero 2026", "Haber de reintegro": "Octubre 2026"},
    {"Haber con descuento": "Marzo 2026", "Haber de reintegro": "Noviembre 2026"},
    {"Haber con descuento": "Abril 2026", "Haber de reintegro": "Diciembre 2026"},
    {"Haber con descuento": "Mayo 2026", "Haber de reintegro": "Enero 2027"},
    {"Haber con descuento": "Junio 2026", "Haber de reintegro": "Febrero 2027"},
    {"Haber con descuento": "Julio 2026", "Haber de reintegro": "Marzo 2027"},
]


def _extra_concepto_412(cargos, anios, zona_porcentaje, escenario):
    if not escenario.get("asignacion_412_extra"):
        return 0.0

    detalle = calcular_asignacion_hora_catedra(
        cargos,
        escenario["valor_indice"],
        anios,
        tasa_funcion_docente=escenario["tasa_funcion_docente"],
        tasa_transformacion_educativa=escenario["tasa_transformacion_educativa"],
    )
    return detalle["asignacionHoraCatedra"]


def calcular_escenario(
    cargos,
    anios,
    zona_porcentaje,
    sindicatos=None,
    descuentos_fijos=0.0,
    escenario=None,
):
    escenario = escenario or ESCENARIO_ACTUAL
    extra_412 = _extra_concepto_412(cargos, anios, zona_porcentaje, escenario)

    calculo = calcular_salario(
        cargos,
        escenario["valor_indice"],
        anios,
        no_remunerativos=0.0,
        incluir_no_remunerativos_automaticos=True,
        descuento_adicional_fijo=descuentos_fijos,
        sindicatos=sindicatos,
        monto_foid_cargo_simple=escenario["monto_foid"],
        monto_material_didactico_cargo_simple=escenario["monto_material"],
        tasa_zona=zona_porcentaje,
        tasa_funcion_docente=escenario["tasa_funcion_docente"],
        tasa_transformacion_educativa=escenario["tasa_transformacion_educativa"],
        otros_remunerativos=extra_412,
        incluir_asignacion_hora_catedra=True,
    )
    calculo["escenario"] = escenario
    calculo["asignacionHoraCatedraExtra"] = extra_412
    return calculo


def calcular_comparacion(
    cargos,
    anios,
    zona_porcentaje,
    sindicatos=None,
    descuentos_fijos=0.0,
):
    actual = calcular_escenario(
        cargos,
        anios,
        zona_porcentaje,
        sindicatos=sindicatos,
        descuentos_fijos=descuentos_fijos,
        escenario=ESCENARIO_ACTUAL,
    )

    filas = []
    for mes in MESES_COMPARACION:
        clave = mes["clave"]
        anterior = calcular_escenario(
            cargos,
            anios,
            zona_porcentaje,
            sindicatos=sindicatos,
            descuentos_fijos=descuentos_fijos,
            escenario=PROPUESTA_ANTERIOR[clave],
        )
        ultima = calcular_escenario(
            cargos,
            anios,
            zona_porcentaje,
            sindicatos=sindicatos,
            descuentos_fijos=descuentos_fijos,
            escenario=PROPUESTA_ULTIMA[clave],
        )
        filas.append(
            {
                **mes,
                "actual": actual,
                "anterior": anterior,
                "ultima": ultima,
                "diferencia_ultima_anterior": ultima["netoFinal"] - anterior["netoFinal"],
                "diferencia_ultima_actual": ultima["netoFinal"] - actual["netoFinal"],
            }
        )

    return {"actual": actual, "filas": filas}


def calcular_proyecciones(
    cargos,
    anios,
    zona_porcentaje,
    sindicatos=None,
    descuentos_fijos=0.0,
):
    """Compatibilidad: devuelve actual + ultima propuesta."""

    resumen = calcular_comparacion(
        cargos,
        anios,
        zona_porcentaje,
        sindicatos=sindicatos,
        descuentos_fijos=descuentos_fijos,
    )
    return [resumen["actual"]] + [fila["ultima"] for fila in resumen["filas"]]


ESCENARIOS = [ESCENARIO_ACTUAL, *PROPUESTA_ULTIMA.values()]
