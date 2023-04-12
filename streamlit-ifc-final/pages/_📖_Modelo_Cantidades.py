import streamlit as st
from tools import ifchelper
from tools import pandashelper
from tools import graph_maker

session = st.session_state

def initialize_session_state():
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

def load_data():
    if "ifc_file" in session:
        session["DataFrame"] = get_ifc_pandas()
        session.Classes = session.DataFrame["Class"].value_counts().keys().tolist()
        session["IsDataFrameLoaded"] = True

def get_ifc_pandas():
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file, 
        "IfcBuildingElement"
    )
    frame = ifchelper.create_pandas_dataframe(data, pset_attributes)
    return frame

def download_csv():
    pandashelper.download_csv(session.file_name,session.DataFrame)

def download_excel():
    pandashelper.download_excel(session.file_name,session.DataFrame)

def execute():  
    st.set_page_config(
        page_title="Quantities",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.subheader(" 🧮 Modelo de Cantidades")
    if not "IsDataFrameLoaded" in session:
        initialize_session_state()
    if not session.IsDataFrameLoaded:
        load_data()
    if session.IsDataFrameLoaded:    
        tab1, tab2 = st.tabs(["Utilidades para Dataframe", "Revisar Cantidades"])
        with tab1:
            ## DATAFRAME REVIEW            
            st.header("Despliegue de Dataframe")  
            st.write(session.DataFrame)
            # from st_aggrid import AgGrid
            # AgGrid(session.DataFrame)
            st.button("Descargar CSV", key="download_csv", on_click=download_csv)
            st.button("Descargar Excel", key="download_excel", on_click=download_excel)
        with tab2:
            row2col1, row2col2 = st.columns(2)
            with row2col1:
                if session.IsDataFrameLoaded:
                    class_selector = st.selectbox("Seleccionar Clase", session.Classes, key="class_selector")
                    session["filtered_frame"] = pandashelper.filter_dataframe_per_class(session.DataFrame, session.class_selector)
                    session["qtos"] = pandashelper.get_qsets_columns(session["filtered_frame"])
                    if session["qtos"] is not None:
                        qto_selector = st.selectbox("Seleccionar Set de Cantidad ", session.qtos, key='qto_selector')
                        quantities = pandashelper.get_quantities(session.filtered_frame, session.qto_selector)
                        st.selectbox("Seleccionar Cantidad", quantities, key="quantity_selector")
                        st.radio('Dividir en', ['Level', 'Type'], key="split_options")
                    else:
                        st.warning("NO hay cantidades!")
            ## DRAW FRAME
            with row2col2: 
                if "quantity_selector" in session and session.quantity_selector == "Count":
                    total = pandashelper.get_total(session.filtered_frame)
                    st.write(f"El numero total de {session.class_selector} es {total}")
                else:
                    if session.qtos is not None:
                        st.subheader(f"{session.class_selector} {session.quantity_selector}")
                        graph = graph_maker.load_graph(
                            session.filtered_frame,
                            session.qto_selector,
                            session.quantity_selector,
                            session.split_options,                                
                        )
                        st.plotly_chart(graph)
    else: 
        st.header("Paso 1: Carge el modelo BIM IFC desde la página de inicio")
    
execute()