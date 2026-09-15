from __future__ import annotations

import base64
from pathlib import Path

import pandas as pd
import streamlit as st

from acumulacion import evaluar_acumulacion
from cargos import (
    ajustar_bonificacion_docente_por_ubicacion,
    cargar_cargos_desde_xlsx,
    etiqueta_cargo,
)
from configuracion import DETALLE_ZONAS_REFERENCIA, ZONAS_REFERENCIA
from descuentos import SINDICATOS
from formato import moneda, porcentaje
from oferta_paritaria import (
    CRONOGRAMA_RESTITUCION_DESCUENTOS,
    MESES_COMPARACION,
    calcular_comparacion,
)


st.set_page_config(
    page_title="Comparador propuestas salariales AMET TDF",
    page_icon="%",
    layout="wide",
)


def _imagen_base64(ruta: str) -> str:
    archivo = Path(__file__).with_name(ruta)
    if not archivo.exists():
        return ""
    return base64.b64encode(archivo.read_bytes()).decode("ascii")


def _css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #14213d;
            --muted: #64748b;
            --line: rgba(20, 33, 61, 0.14);
            --blue: #0437ff;
            --cyan: #0fb9c8;
            --green: #0f8f75;
            --amber: #f59e0b;
            --rose: #f43f5e;
            --soft-blue: #eef6ff;
            --soft-green: #eafaf5;
        }
        .stApp {
            background:
                linear-gradient(120deg, rgba(4,55,255,0.10), rgba(15,185,200,0.08) 38%, #ffffff 72%);
            color: var(--ink);
        }
        .block-container {
            max-width: 1220px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }
        .hero {
            display: grid;
            grid-template-columns: 260px minmax(0, 1fr);
            align-items: center;
            gap: 1.6rem;
            padding: 1.7rem 1.9rem;
            margin-bottom: 1.2rem;
            border-radius: 14px;
            overflow: hidden;
            color: #ffffff;
            background:
                radial-gradient(circle at 90% 30%, rgba(255,255,255,0.20), transparent 30%),
                linear-gradient(100deg, #0617ff 0%, #064ddc 46%, #13bdc3 100%);
            box-shadow: 0 20px 48px rgba(4, 55, 255, 0.18);
        }
        .hero-logo {
            width: 100%;
            max-height: 108px;
            object-fit: contain;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.45rem;
            line-height: 1.02;
            letter-spacing: 0;
            color: #ffffff;
        }
        .hero p {
            margin: 0.65rem 0 0;
            max-width: 820px;
            color: rgba(255,255,255,0.88);
            font-size: 1rem;
            line-height: 1.45;
        }
        .kicker {
            display: inline-flex;
            margin-bottom: 0.65rem;
            padding: 0.28rem 0.7rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.16);
            color: #ffffff;
            font-size: 0.78rem;
            font-weight: 800;
        }
        .intro-card,
        .result-card,
        .mini-card {
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.92);
            border-radius: 12px;
            box-shadow: 0 14px 34px rgba(20,33,61,0.07);
        }
        .intro-card {
            padding: 1.05rem 1.15rem;
            margin-bottom: 1rem;
        }
        .intro-card strong {
            color: var(--ink);
        }
        .intro-card span {
            display: inline-block;
            margin: 0.25rem 0.35rem 0.25rem 0;
            padding: 0.35rem 0.55rem;
            border-radius: 999px;
            background: var(--soft-blue);
            color: #075985;
            font-size: 0.82rem;
            font-weight: 700;
        }
        .result-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 0.9rem 0 1rem;
        }
        .result-card {
            min-height: 168px;
            padding: 1.1rem;
            border-color: rgba(4,55,255,0.22);
        }
        .result-card.current {
            background: linear-gradient(145deg, #ffffff, #f6f8fb);
        }
        .result-card.previous {
            border-color: rgba(245,158,11,0.36);
            background: linear-gradient(145deg, rgba(255,247,237,0.88), #ffffff);
        }
        .result-card.latest {
            border-color: rgba(15,143,117,0.45);
            background: linear-gradient(145deg, rgba(234,250,245,0.95), #ffffff);
        }
        .result-card strong {
            display: block;
            color: var(--ink);
            font-size: 0.95rem;
            margin-bottom: 0.35rem;
        }
        .result-card .money {
            display: block;
            color: var(--ink);
            font-size: clamp(1.45rem, 2.3vw, 2rem);
            line-height: 1.08;
            font-weight: 850;
            letter-spacing: 0;
            overflow-wrap: anywhere;
        }
        .result-card.latest .money {
            color: var(--green);
        }
        .result-card small {
            display: block;
            margin-top: 0.55rem;
            color: var(--muted);
            line-height: 1.35;
        }
        .delta-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.85rem;
            margin: 0.3rem 0 1.2rem;
        }
        .mini-card {
            padding: 0.9rem 1rem;
        }
        .mini-card strong {
            color: var(--muted);
            font-size: 0.86rem;
        }
        .mini-card span {
            display: block;
            margin-top: 0.25rem;
            color: var(--ink);
            font-size: 1.25rem;
            font-weight: 800;
        }
        .mini-card.good span {
            color: var(--green);
        }
        .mini-card.warn span {
            color: var(--amber);
        }
        div[data-testid="stAlert"] {
            border-radius: 10px;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255,255,255,0.68);
        }
        @media (max-width: 900px) {
            .hero {
                grid-template-columns: 1fr;
                padding: 1.35rem;
            }
            .hero-logo {
                max-width: 210px;
            }
            .hero h1 {
                font-size: 2rem;
            }
            .result-grid,
            .delta-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _hero() -> None:
    logo = _imagen_base64("logo_amet_tdf_transparente.png")
    logo_html = (
        f'<img class="hero-logo" src="data:image/png;base64,{logo}" alt="AMET TDF">'
        if logo
        else ""
    )
    st.markdown(
        f"""
        <div class="hero">
            {logo_html}
            <div>
                <div class="kicker">AMET REGIONAL XXIV TIERRA DEL FUEGO A.I.A.S.</div>
                <h1>Comparador de propuestas salariales</h1>
                <p>Calcula la misma carga docente contra tres referencias: sueldo actual cobrado, propuesta anterior rechazada y última propuesta paritaria.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _panel_inicio() -> None:
    st.markdown(
        """
        <div class="intro-card">
            <strong>Qué compara este calculador</strong><br>
            <span>Actual: haberes agosto 2026</span>
            <span>Anterior: FD 239%, VI +1% escalonado, FOID $100.000</span>
            <span>Última: FD 255%, 265%, 270% y 285%; FOID $70.000/$90.000</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _tarjetas_principales(actual: dict, anterior: dict, ultima: dict, fila: dict) -> None:
    st.markdown(
        f"""
        <div class="result-grid">
            <div class="result-card current">
                <strong>Actual cobrado</strong>
                <span class="money">{moneda(actual["netoFinal"])}</span>
                <small>Haberes agosto 2026, cobrados en septiembre. Es la base de comparación.</small>
            </div>
            <div class="result-card previous">
                <strong>Propuesta anterior</strong>
                <span class="money">{moneda(anterior["netoFinal"])}</span>
                <small>{fila["mes_haber"]}, cobro {fila["mes_cobro"]}. {anterior["escenario"]["detalle"]}</small>
            </div>
            <div class="result-card latest">
                <strong>Última propuesta</strong>
                <span class="money">{moneda(ultima["netoFinal"])}</span>
                <small>{fila["mes_haber"]}, cobro {fila["mes_cobro"]}. {ultima["escenario"]["detalle"]}</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _tarjetas_diferencias(actual: dict, anterior: dict, ultima: dict) -> None:
    diferencia_vs_actual = ultima["netoFinal"] - actual["netoFinal"]
    diferencia_vs_anterior = ultima["netoFinal"] - anterior["netoFinal"]
    porcentaje_vs_actual = diferencia_vs_actual / actual["netoFinal"] if actual["netoFinal"] else 0.0
    porcentaje_vs_anterior = diferencia_vs_anterior / anterior["netoFinal"] if anterior["netoFinal"] else 0.0
    clase_anterior = "good" if diferencia_vs_anterior >= 0 else "warn"
    clase_actual = "good" if diferencia_vs_actual >= 0 else "warn"

    st.markdown(
        f"""
        <div class="delta-grid">
            <div class="mini-card {clase_anterior}">
                <strong>Última propuesta vs propuesta anterior</strong>
                <span>{moneda(diferencia_vs_anterior)}</span>
                <small>{porcentaje(porcentaje_vs_anterior)} sobre la propuesta anterior.</small>
            </div>
            <div class="mini-card {clase_actual}">
                <strong>Última propuesta vs sueldo actual</strong>
                <span>{moneda(diferencia_vs_actual)}</span>
                <small>{porcentaje(porcentaje_vs_actual)} sobre lo cobrado por agosto.</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _tabla_meses(resumen: dict) -> pd.DataFrame:
    actual = resumen["actual"]
    anterior_previo = actual["netoFinal"]
    ultima_previa = actual["netoFinal"]
    filas = []
    for fila in resumen["filas"]:
        anterior = fila["anterior"]
        ultima = fila["ultima"]
        filas.append(
            {
                "Mes de cobro": fila["mes_cobro"],
                "Haberes liquidados": fila["mes_haber"],
                "Actual sin cambios": moneda(actual["netoFinal"]),
                "Rechazada agosto": moneda(anterior["netoFinal"]),
                "Nueva propuesta": moneda(ultima["netoFinal"]),
                "Movimiento rechazada": moneda(anterior["netoFinal"] - anterior_previo),
                "Movimiento nueva": moneda(ultima["netoFinal"] - ultima_previa),
                "Nueva vs rechazada": moneda(fila["diferencia_ultima_anterior"]),
                "Nueva vs actual": moneda(fila["diferencia_ultima_actual"]),
            }
        )
        anterior_previo = anterior["netoFinal"]
        ultima_previa = ultima["netoFinal"]
    return pd.DataFrame(filas)


def _tabla_cambios(resumen: dict) -> pd.DataFrame:
    filas = []
    for fila in resumen["filas"]:
        filas.append(
            {
                "Mes de cobro": fila["mes_cobro"],
                "Rechazada agosto": fila["anterior"]["escenario"]["detalle"],
                "Nueva propuesta": fila["ultima"]["escenario"]["detalle"],
            }
        )
    return pd.DataFrame(filas)


def _tabla_componentes(calculo: dict) -> pd.DataFrame:
    componentes = calculo["componentes"]
    filas = [
        ("Básico", componentes["basico"]),
        ("Antigüedad", componentes["antiguedad"]),
        ("Función Docente", componentes["funcionDocente"]),
        ("Bonificación Docente", componentes["bonificacionDocente"]),
        ("Adicional Jerárquico", componentes["adicionalJerarquico"]),
        ("Zona", componentes["zona"]),
        ("Transformación Educativa", componentes["transformacionEducativa"]),
        ("Asignación Hora Cátedra", calculo["asignacionHoraCatedra"]),
    ]
    if calculo.get("asignacionHoraCatedraExtra"):
        filas.append(("Asignación 412 adicional anterior", calculo["asignacionHoraCatedraExtra"]))
    filas.extend(
        [
            ("Bruto remunerativo", calculo["brutoRemunerativo"]),
            ("Jubilación", calculo["descuentosLegales"]["jubilacion"]),
            ("Obra social", calculo["descuentosLegales"]["obra_social"]),
            ("Seguro de vida", calculo["descuentosLegales"]["seguro_vida"]),
            ("Descuento sindical", calculo["descuentosSindicales"]["total"]),
            ("Descuentos totales", calculo["descuentosTotales"]),
            ("Neto sin no remunerativos", calculo["netoSinNoRemunerativos"]),
            ("FOID automático", calculo["noRemunerativosAutomaticosDetalle"]["foid"]),
            (
                "Material didáctico automático",
                calculo["noRemunerativosAutomaticosDetalle"]["materialDidactico"],
            ),
            ("No remunerativos total", calculo["noRemunerativos"]),
            ("Neto final", calculo["netoFinal"]),
        ]
    )
    return pd.DataFrame([{"Concepto": nombre, "Monto": moneda(monto)} for nombre, monto in filas])


def _detalle_calculo(resumen: dict, fila_seleccionada: dict) -> None:
    with st.expander("Ver detalle del cálculo"):
        opciones = {
            "Actual cobrado": resumen["actual"],
            "Propuesta anterior": fila_seleccionada["anterior"],
            "Última propuesta": fila_seleccionada["ultima"],
        }
        nombre = st.selectbox("Escenario a revisar", list(opciones.keys()))
        calculo = opciones[nombre]
        st.caption(calculo["escenario"]["detalle"])
        st.dataframe(_tabla_componentes(calculo), use_container_width=True, hide_index=True)

        detalle_cargos = calculo.get("detalleCargos", [])
        if detalle_cargos:
            st.markdown("#### Cargos y horas cargados")
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Código": item["codigoCargo"],
                            "Descripción": item["descripcion"],
                            "Cantidad": item["cantidad"],
                            "Puntaje unitario": item["puntajeCargo"],
                            "Puntaje total": item["puntajeTotal"],
                            "Básico": moneda(item["basico"]),
                            "Bonif. docente": moneda(item["bonificacionDocente"]),
                            "Adic. jerárquico": moneda(item["adicionalJerarquico"]),
                        }
                        for item in detalle_cargos
                    ]
                ),
                use_container_width=True,
                hide_index=True,
            )

        sindicales = calculo.get("descuentosSindicales", {})
        detalle_sindical = sindicales.get("detalle", [])
        if detalle_sindical:
            st.markdown("#### Descuento sindical")
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Sindicato": item["sindicato"],
                            "Sobre remunerativo": porcentaje(item["tasa_remunerativo"]),
                            "Monto remunerativo": moneda(item["monto_remunerativo"]),
                            "Sobre FOID": porcentaje(item["tasa_foid"]),
                            "Monto FOID": moneda(item["monto_foid"]),
                            "Total": moneda(item["total"]),
                        }
                        for item in detalle_sindical
                    ]
                ),
                use_container_width=True,
                hide_index=True,
            )


def _cronograma_restitucion() -> None:
    with st.expander("Restitución de descuentos mencionada en el acta"):
        st.caption(
            "Cronograma informativo. No se suma al neto porque depende de descuentos previos de cada docente."
        )
        st.dataframe(
            pd.DataFrame(CRONOGRAMA_RESTITUCION_DESCUENTOS),
            use_container_width=True,
            hide_index=True,
        )


@st.cache_data
def _cargos_disponibles() -> list[dict]:
    return cargar_cargos_desde_xlsx()


_css()
_hero()
_panel_inicio()

cargos_disponibles = _cargos_disponibles()
opciones = [etiqueta_cargo(cargo) for cargo in cargos_disponibles]
mapa_cargos = dict(zip(opciones, cargos_disponibles))
opcion_212 = next((opcion for opcion in opciones if opcion.startswith("212 -")), opciones[0])
meses = {f'{m["mes_haber"]} / cobro {m["mes_cobro"]}': m["clave"] for m in MESES_COMPARACION}

col_izq, col_der = st.columns([0.95, 1.55], gap="large")

with col_izq:
    st.markdown("### 1. Ubicación y antigüedad")
    ubicacion = st.selectbox("Ubicación de zona", list(ZONAS_REFERENCIA.keys()))
    tasa_zona = ZONAS_REFERENCIA[ubicacion]
    st.info(f"{DETALLE_ZONAS_REFERENCIA[ubicacion]}.")
    anios_antiguedad = st.number_input(
        "Años de antigüedad reconocidos",
        min_value=0,
        max_value=50,
        value=0,
        step=1,
    )

    st.markdown("### 2. Descuento sindical")
    sindicatos = st.multiselect(
        "Sindicato/s",
        list(SINDICATOS.keys()),
        help="Seleccione hasta tres sindicatos. Si no corresponde, deje vacío.",
    )
    if len(sindicatos) > 3:
        st.warning("Se toman solo los primeros tres sindicatos seleccionados.")
        sindicatos = sindicatos[:3]

with col_der:
    st.markdown("### 3. Cargos u horas cátedra")
    cantidad_lineas = st.number_input(
        "Cantidad de cargos u horas cátedra a incorporar",
        min_value=1,
        max_value=10,
        value=1,
        step=1,
    )

    cargos_seleccionados = []
    for indice in range(int(cantidad_lineas)):
        c1, c2 = st.columns([0.78, 0.22], gap="medium")
        with c1:
            opcion = st.selectbox(
                f"Cargo / hora {indice + 1}",
                opciones,
                index=opciones.index(opcion_212),
                key=f"cargo_{indice}",
                help="Escriba el código o parte del nombre dentro del selector para filtrar.",
            )
        with c2:
            cantidad = st.number_input(
                "Cantidad",
                min_value=1.0,
                max_value=80.0,
                value=1.0,
                step=1.0,
                key=f"cantidad_{indice}",
            )
        cargo = ajustar_bonificacion_docente_por_ubicacion(mapa_cargos[opcion], ubicacion)
        cargo = dict(cargo)
        cargo["cantidad"] = cantidad
        cargos_seleccionados.append(cargo)

evaluacion = evaluar_acumulacion(cargos_seleccionados)
if evaluacion["estado"] == "advertencia":
    for advertencia in evaluacion["advertencias"]:
        st.warning(advertencia)
else:
    st.info(
        "Control Ley 761: con la carga ingresada no aparece una advertencia básica de exceso. "
        "Este control es orientativo."
    )

resumen = calcular_comparacion(
    cargos_seleccionados,
    int(anios_antiguedad),
    tasa_zona,
    sindicatos=sindicatos,
)

st.markdown("## Planilla de evolución octubre-febrero")
st.info(
    "La columna 'Actual sin cambios' mantiene fijo lo cobrado por agosto para usarlo como base. "
    "Las otras dos columnas muestran cómo hubiera evolucionado la propuesta rechazada y cómo evoluciona la nueva propuesta."
)
st.dataframe(_tabla_meses(resumen), use_container_width=True, hide_index=True)

st.markdown("### Resumen del mes seleccionado")
mes_label = st.selectbox(
    "Elegir mes para ver los tres valores grandes",
    list(meses.keys()),
    index=0,
    help="El sueldo de cada mes de haber se cobra al mes siguiente.",
)
clave_mes = meses[mes_label]
fila_seleccionada = next(fila for fila in resumen["filas"] if fila["clave"] == clave_mes)
actual = resumen["actual"]
anterior = fila_seleccionada["anterior"]
ultima = fila_seleccionada["ultima"]

_tarjetas_principales(actual, anterior, ultima, fila_seleccionada)
_tarjetas_diferencias(actual, anterior, ultima)

with st.expander("Ver qué cambia en cada mes"):
    st.dataframe(_tabla_cambios(resumen), use_container_width=True, hide_index=True)

st.info(
    "La restitución de descuentos se muestra aparte y no se suma automáticamente, porque depende de cada recibo."
)
_detalle_calculo(resumen, fila_seleccionada)
_cronograma_restitucion()

st.caption(
    "Simulación orientativa para análisis gremial. Los valores definitivos dependen de la liquidación oficial y de situaciones particulares de cada recibo."
)
