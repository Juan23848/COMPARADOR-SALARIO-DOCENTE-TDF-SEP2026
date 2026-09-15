import unittest

from cargos import buscar_cargo, cargar_cargos_desde_xlsx
from configuracion import MONTO_SEGURO_VIDA_OBLIGATORIO
from oferta_paritaria import (
    CRONOGRAMA_RESTITUCION_DESCUENTOS,
    ESCENARIO_ACTUAL,
    MESES_COMPARACION,
    MONTO_FOID_ANTERIOR,
    MONTO_FOID_ULTIMA_ENERO,
    MONTO_FOID_ULTIMA_NOVIEMBRE,
    PROPUESTA_ANTERIOR,
    PROPUESTA_ULTIMA,
    TASA_FUNCION_DOCENTE_ANTERIOR,
    TASA_FUNCION_DOCENTE_ULTIMA_ENERO,
    TASA_FUNCION_DOCENTE_ULTIMA_NOVIEMBRE,
    TASA_FUNCION_DOCENTE_ULTIMA_OCTUBRE,
    TASA_FUNCION_DOCENTE_ULTIMA_SEPTIEMBRE,
    VALOR_INDICE_ACTUAL,
    calcular_comparacion,
    calcular_escenario,
)


class ComparadorParitariaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cargos = cargar_cargos_desde_xlsx()

    def test_meses_de_comparacion_esperados(self):
        self.assertEqual(
            [(mes["mes_haber"], mes["mes_cobro"]) for mes in MESES_COMPARACION],
            [
                ("Septiembre 2026", "Octubre 2026"),
                ("Octubre 2026", "Noviembre 2026"),
                ("Noviembre 2026", "Diciembre 2026"),
                ("Diciembre 2026", "Enero 2027"),
                ("Enero 2027", "Febrero 2027"),
            ],
        )

    def test_parametros_de_la_ultima_propuesta(self):
        self.assertEqual(
            [escenario["tasa_funcion_docente"] for escenario in PROPUESTA_ULTIMA.values()],
            [
                TASA_FUNCION_DOCENTE_ULTIMA_SEPTIEMBRE,
                TASA_FUNCION_DOCENTE_ULTIMA_OCTUBRE,
                TASA_FUNCION_DOCENTE_ULTIMA_NOVIEMBRE,
                TASA_FUNCION_DOCENTE_ULTIMA_NOVIEMBRE,
                TASA_FUNCION_DOCENTE_ULTIMA_ENERO,
            ],
        )
        self.assertEqual(PROPUESTA_ULTIMA["septiembre_2026"]["monto_foid"], 56000.00)
        self.assertEqual(PROPUESTA_ULTIMA["octubre_2026"]["monto_foid"], 56000.00)
        self.assertEqual(PROPUESTA_ULTIMA["noviembre_2026"]["monto_foid"], MONTO_FOID_ULTIMA_NOVIEMBRE)
        self.assertEqual(PROPUESTA_ULTIMA["diciembre_2026"]["monto_foid"], MONTO_FOID_ULTIMA_NOVIEMBRE)
        self.assertEqual(PROPUESTA_ULTIMA["enero_2027"]["monto_foid"], MONTO_FOID_ULTIMA_ENERO)

    def test_cronograma_restitucion_descuentos(self):
        self.assertEqual(
            CRONOGRAMA_RESTITUCION_DESCUENTOS,
            [
                {"Haber con descuento": "Enero 2026", "Haber de reintegro": "Septiembre 2026"},
                {"Haber con descuento": "Febrero 2026", "Haber de reintegro": "Octubre 2026"},
                {"Haber con descuento": "Marzo 2026", "Haber de reintegro": "Noviembre 2026"},
                {"Haber con descuento": "Abril 2026", "Haber de reintegro": "Diciembre 2026"},
                {"Haber con descuento": "Mayo 2026", "Haber de reintegro": "Enero 2027"},
                {"Haber con descuento": "Junio 2026", "Haber de reintegro": "Febrero 2027"},
                {"Haber con descuento": "Julio 2026", "Haber de reintegro": "Marzo 2027"},
            ],
        )

    def test_parametros_de_la_propuesta_anterior(self):
        self.assertAlmostEqual(PROPUESTA_ANTERIOR["septiembre_2026"]["valor_indice"], VALOR_INDICE_ACTUAL * 1.01)
        self.assertAlmostEqual(PROPUESTA_ANTERIOR["octubre_2026"]["valor_indice"], VALOR_INDICE_ACTUAL * 1.01 * 1.01)
        self.assertAlmostEqual(
            PROPUESTA_ANTERIOR["noviembre_2026"]["valor_indice"],
            VALOR_INDICE_ACTUAL * 1.01 * 1.01 * 1.01,
        )
        self.assertAlmostEqual(
            PROPUESTA_ANTERIOR["diciembre_2026"]["valor_indice"],
            VALOR_INDICE_ACTUAL * 1.01 * 1.01 * 1.01,
        )
        self.assertEqual(PROPUESTA_ANTERIOR["enero_2027"]["monto_foid"], MONTO_FOID_ANTERIOR)
        self.assertEqual(
            PROPUESTA_ANTERIOR["enero_2027"]["tasa_funcion_docente"],
            TASA_FUNCION_DOCENTE_ANTERIOR,
        )
        self.assertTrue(PROPUESTA_ANTERIOR["enero_2027"]["asignacion_412_extra"])

    def test_foid_y_seguro_del_actual(self):
        cargo = dict(buscar_cargo(self.cargos, "212"))
        cargo["cantidad"] = 1
        actual = calcular_escenario([cargo], 0, 1.0, [], escenario=ESCENARIO_ACTUAL)

        self.assertEqual(actual["noRemunerativosAutomaticosDetalle"]["foid"], 56000.00)
        self.assertEqual(actual["descuentosLegales"]["seguro_vida"], 4400.00)
        self.assertEqual(MONTO_SEGURO_VIDA_OBLIGATORIO, 4400.00)

    def test_ultima_propuesta_mejora_enero_frente_a_actual(self):
        cargo = dict(buscar_cargo(self.cargos, "212"))
        cargo["cantidad"] = 1
        resumen = calcular_comparacion([cargo], 0, 1.0, sindicatos=[])
        enero = resumen["filas"][-1]

        self.assertGreater(enero["ultima"]["netoFinal"], resumen["actual"]["netoFinal"])
        self.assertGreater(enero["ultima"]["componentes"]["funcionDocente"], resumen["actual"]["componentes"]["funcionDocente"])


if __name__ == "__main__":
    unittest.main()
