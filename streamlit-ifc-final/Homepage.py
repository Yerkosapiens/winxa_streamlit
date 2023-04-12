import ifcopenshell
import streamlit as st

def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True
    
    ### Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name

def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
        st.balloons()

def main():      
    st.set_page_config(
        layout= "wide",
        page_title="Winxa Sistemas de Ingenieria",
        page_icon="✍️",
    )
    st.header("WINXA Sistemas de Ingeniaría") 
    st.subheader("")
    st.markdown(
    """ 
    ###  📁 Haga click en el botón CARGAR MODELO para comenzar
    """
    )

    ## Add File uploader to Side Bar Navigation
    st.sidebar.header('CARGAR MODELO BIM')
    st.sidebar.file_uploader("Seleccionar archivo", type=['ifc'], key="uploaded_file", on_change=callback_upload)

    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success(f'Projecto cargado exitosamente')
        st.sidebar.write("🔃 Puede recargar un nuevo archivo  ")
        
        col1, col2 = st.columns([2,1])
        col1.subheader(f'Proyecto "{get_project_name()}"')
        col2.text_input("✏️ Editar Nombre del Proyecto", key="project_name_input")
        col2.button("✔️ Aplicar", key="change_project_name", on_click=change_project_name())

    st.sidebar.write("""
    --------------
    ### Derechos Reservados:
    #### Winxa Sistemas de Ingeniería (MR)
    
       
    """)
    st.write("")
    st.sidebar.write("")

if __name__ == "__main__":
    session = st.session_state
    main()