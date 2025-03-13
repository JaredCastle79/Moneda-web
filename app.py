import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado que se conservan entre ejecuciones
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

# Título de la aplicación
st.header('Lanzar una moneda')

# Gráfico de líneas para mostrar el progreso de la media
chart = st.line_chart([0.5])

# Función para simular el lanzamiento de una moneda
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)  # Pequeña pausa para visualizar el progreso

    return mean

# Widgets de entrada
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

# Lógica al presionar el botón "Ejecutar"
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    
    # Incrementar el número de experimento
    st.session_state['experiment_no'] += 1
    
    # Simular los lanzamientos y calcular la media
    mean = toss_coin(number_of_trials)
    
    # Guardar los resultados en el DataFrame
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iteraciones', 'media'])
    ], axis=0)
    
    # Reiniciar el índice del DataFrame
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

# Mostrar la tabla de resultados
st.write(st.session_state['df_experiment_results'])
