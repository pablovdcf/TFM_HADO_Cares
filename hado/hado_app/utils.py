# Functions and utility classes
import streamlit as st
    
        
def ui_spacer(n=2, line=False, next_n=0):
	for _ in range(n):
		st.write('')
	if line:
		st.tabs([' '])
	for _ in range(next_n):
		st.write('')

def ui_info():
	st.markdown(f"""
	# HADO CARES
	""")
	ui_spacer(1)
	st.write("Made by [Pablo Villar del Castillo](https://www.linkedin.com/in/pablovillardelcastillo/).", unsafe_allow_html=True)
	ui_spacer(1)
	st.markdown("""
		Gracias por su interés en mi aplicación.
		Tenga en cuenta que esto es sólo una aplicación de prueba
		y puede contener errores o características sin terminar.
		""")
	ui_spacer(1)
	st.markdown('El código fuente está disponible [aquí](https://github.com/pablovdcf/TFM_HADO_Cares).')