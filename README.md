# Comparador de propuestas salariales AMET TDF

Aplicacion Streamlit independiente para comparar una misma carga docente contra tres referencias:

- Actual cobrado: haberes de agosto 2026.
- Propuesta anterior rechazada: Funcion Docente 239%, Valor Indice +1% escalonado, FOID $100.000 y asignacion 412 adicional en enero.
- Ultima propuesta: Funcion Docente 255%, 265%, 270% y 285%; FOID $70.000 desde noviembre y $90.000 desde enero.

## Ejecutar localmente

```powershell
python -m streamlit run app.py
```

## Criterio de meses

El selector muestra el mes del haber y aclara en que mes se cobra. La restitucion de descuentos mencionada en el acta se muestra como informacion aparte y no se suma automaticamente al neto.
