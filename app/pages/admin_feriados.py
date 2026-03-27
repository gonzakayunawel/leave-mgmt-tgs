import streamlit as st
from datetime import date
from app.database import get_feriados_internos, add_feriado_interno, delete_feriado_interno


def render_admin_feriados(user):
    """Página para que el admin gestione los días no laborables internos."""
    st.header("📅 Días No Laborables Internos")
    st.caption(
        "Define fechas específicas en las que no se permite solicitar permisos "
        "(ej. cierre de año, feriados propios del establecimiento)."
    )

    feriados = get_feriados_internos()

    # --- Lista de feriados actuales ---
    if feriados:
        st.subheader("Días registrados")
        for f in feriados:
            col_fecha, col_desc, col_btn = st.columns([2, 5, 1])
            col_fecha.write(f["fecha"])
            col_desc.write(f.get("descripcion") or "—")
            if col_btn.button("🗑️", key=f"del_{f['id']}", help="Eliminar", disabled=is_read_only):
                delete_feriado_interno(f["id"])
                st.rerun()
    else:
        st.info("No hay días no laborables internos registrados.")

    st.divider()

    # --- Formulario para agregar ---
    st.subheader("Agregar día no laborable")
    with st.form("form_feriado"):
        nueva_fecha = st.date_input(
            "Fecha",
            min_value=date.today(),
            max_value=date(date.today().year + 2, 12, 31),
            disabled=is_read_only
        )
        descripcion = st.text_input("Descripción (opcional)", max_chars=100,
                                    placeholder="ej. Cierre fin de año escolar",
                                    disabled=is_read_only)
        guardar = st.form_submit_button("Guardar", icon="💾", disabled=is_read_only)

        if guardar:
            fechas_existentes = {f["fecha"] for f in feriados}
            if str(nueva_fecha) in fechas_existentes:
                st.error("Esa fecha ya está registrada.")
            else:
                add_feriado_interno(str(nueva_fecha), descripcion.strip(), user["id"])
                st.success(f"Día no laborable {nueva_fecha} agregado correctamente.")
                st.rerun()
)
                st.rerun()
