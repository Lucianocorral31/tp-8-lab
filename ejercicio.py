import pandas as pd  
import numpy as np  
import streamlit as st  
import matplotlib.pyplot as plt  
from scipy import stats  

# Función para mostrar los detalles del estudiante  
def mostrar_detalles_usuario():  
    st.write("Por favor, sube un archivo CSV desde la barra lateral.")  
    st.markdown("#### Información del Alumno")  
    st.markdown("**Legajo:** 59158")  
    st.markdown("**Nombre Completo:** Luciano Corral")  
    st.markdown("**Comisión:** C7")  

# Función para cargar archivo CSV en el panel lateral  
def cargar_datos_csv():  
    st.sidebar.title("Carga de Datos CSV")  
    archivo = st.sidebar.file_uploader("Selecciona tu archivo CSV", type="csv")  
    if archivo:  
        return pd.read_csv(archivo)  
    return None  

# Función para procesar los datos y generar gráficos  
def mostrar_metricas_y_graficos(datos, sucursal_seleccionada):  
    if sucursal_seleccionada != "Todas":  
        datos = datos[datos["Sucursal"] == sucursal_seleccionada]  

    productos_distintos = datos["Producto"].unique()  

    for producto in productos_distintos:  
        datos_producto = datos[datos["Producto"] == producto]  

        # Calcular métricas  
        unidades_totales = datos_producto["Unidades_vendidas"].sum()  
        ingresos_totales = datos_producto["Ingreso_total"].sum()  
        costos_totales = datos_producto["Costo_total"].sum()  

        precio_unitario_promedio = (ingresos_totales / unidades_totales) if unidades_totales > 0 else 0  
        margen_unitario_promedio = (ingresos_totales - costos_totales) / ingresos_totales * 100 if ingresos_totales > 0 else 0  

        # Mostrar las métricas en un contenedor  
        st.container()  
        col1, col2 = st.columns([1, 3])  
        
        with col1:  
            st.metric(label="Precio Promedio", value=f"${precio_unitario_promedio:,.2f}")  
            st.metric(label="Margen Promedio", value=f"{margen_unitario_promedio:.2f}%")  
            st.metric(label="Unidades Vendidas", value=f"{unidades_totales:,.0f}")  

        with col2:  
            mostrar_grafico_evolucion(datos_producto, producto)  

# Función para mostrar el gráfico de evolución de ventas  
def mostrar_grafico_evolucion(datos_producto, producto):  
    datos_producto['Fecha'] = pd.to_datetime(datos_producto['Año'].astype(str) + '-' + datos_producto['Mes'].astype(str) + '-01')  
    datos_producto.sort_values('Fecha', inplace=True)  

    fig, ax = plt.subplots()  
    ax.plot(datos_producto['Fecha'], datos_producto['Unidades_vendidas'], label=f"Ventas de {producto}", color='royalblue')  

    # Línea de tendencia  
    x = np.arange(len(datos_producto))  
    y = datos_producto["Unidades_vendidas"].values  
    slope, intercept, _, _, _ = stats.linregress(x, y)  
    tendencia = slope * x + intercept  
    ax.plot(datos_producto['Fecha'], tendencia, label="Tendencia", linestyle='--', color='tomato')  

    ax.set_title(f"Evolución de Ventas Mensuales - {producto}")  
    ax.set_xlabel("Mes")  
    ax.set_ylabel("Unidades Vendidas")  
    ax.legend()  

    st.pyplot(fig)  

# Función principal para ejecutar la aplicación  
def ejecutar_app():  
    # Configuración de la página  
    st.set_page_config(page_title="Análisis de Ventas", layout="wide")  

    # Cargar los datos  
    datos = cargar_datos_csv()  

    if datos is not None:  
        # Selección de sucursal  
        sucursales_disponibles = ["Todas"] + datos["Sucursal"].unique().tolist()  
        sucursal_seleccionada = st.sidebar.selectbox("Selecciona la Sucursal para análisis", sucursales_disponibles)  

        # Mostrar métricas y gráficos  
        mostrar_metricas_y_graficos(datos, sucursal_seleccionada)  
    else:  
        mostrar_detalles_usuario()  

if __name__ == "__main__":  
    ejecutar_app()  