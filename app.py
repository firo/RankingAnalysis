import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Titolo dell'applicazione
st.title('Analisi della Classifica delle Azioni')

# Caricamento del file CSV
uploaded_file = st.file_uploader("Carica il file CSV", type="csv")

# Verifica se il file è stato caricato
if uploaded_file is not None:
    # Lettura del file CSV
    df = pd.read_csv(uploaded_file)
    
    # Visualizzazione del dataset
    st.write("Dataset caricato:")
    st.dataframe(df)
    
    # Pulizia e trasformazione dei dati
    df['Fair Value (%)'] = df['Fair Value (%)'].astype(str)
    df['Fair Value (%)'] = df['Fair Value (%)'].str.strip().str.replace('+', '').astype(float)
    df['M-Score'] = df['M-Score'].astype(float)
    
    # Sidebar per filtrare i dati
    st.sidebar.title("Filtri")
    
    fair_value_filter = st.sidebar.slider('Filtro per Fair Value (%)', float(df['Fair Value (%)'].min()), float(df['Fair Value (%)'].max()), (float(df['Fair Value (%)'].min()), float(df['Fair Value (%)'].max())))
    z_score_filter = st.sidebar.slider('Filtro per Z-Score', float(df['Z-Score'].min()), float(df['Z-Score'].max()), (float(df['Z-Score'].min()), float(df['Z-Score'].max())))
    f_score_filter = st.sidebar.slider('Filtro per F-Score', int(df['F-Score'].min()), int(df['F-Score'].max()), (int(df['F-Score'].min()), int(df['F-Score'].max())))
    m_score_filter = st.sidebar.slider('Filtro per M-Score', float(df['M-Score'].min()), float(df['M-Score'].max()), (float(df['M-Score'].min()), float(df['M-Score'].max())))
    value_generation_filter = st.sidebar.multiselect('Filtro per Value Generation', df['Value Generation'].unique(), df['Value Generation'].unique())
    
    # Applicazione dei filtri
    filtered_df = df[
        (df['Fair Value (%)'] >= fair_value_filter[0]) & (df['Fair Value (%)'] <= fair_value_filter[1]) &
        (df['Z-Score'] >= z_score_filter[0]) & (df['Z-Score'] <= z_score_filter[1]) &
        (df['F-Score'] >= f_score_filter[0]) & (df['F-Score'] <= f_score_filter[1]) &
        (df['M-Score'] >= m_score_filter[0]) & (df['M-Score'] <= m_score_filter[1]) &
        (df['Value Generation'].isin(value_generation_filter))
    ]
    
    st.write("Dataset filtrato:")
    st.dataframe(filtered_df)

    # Scatter Plot per Fair Value
    st.subheader('Fair Value (%) by Stock')
    plt.figure(figsize=(14, 8))
    sns.scatterplot(data=filtered_df, x='Stock', y='Fair Value (%)', hue='Value Generation', palette='viridis', s=100)
    plt.xticks(rotation=90)
    plt.title('Fair Value (%) by Stock')
    st.pyplot(plt)
    plt.clf()  # Pulisci la figura per evitare sovrapposizioni

    # Scatter Plot per Fair value e z-score
    st.subheader('Fair Value vs Z-Score')
    plt.figure(figsize=(14, 8))
    sns.scatterplot(data=filtered_df, x='Z-Score', y='Fair Value (%)', hue='Value Generation', palette='viridis', alpha=0.7)
    plt.xlabel('Z-Score')
    plt.ylabel('Fair Value (%)')
    plt.legend(title='Value Generation', loc='upper right')
    plt.grid(True)
    plt.title('Fair Value vs Z-Score')
    st.pyplot(plt)
    plt.clf()  # Pulisci la figura per evitare sovrapposizioni
    
    # Box Plot per Z-Score
    st.subheader('Distribution of Z-Score by Stock')
    plt.figure(figsize=(14, 8))
    sns.scatterplot(data=filtered_df, x='Stock', y='Z-Score')
    plt.xticks(rotation=90)
    plt.title('Distribution of Z-Score by Stock')
    st.pyplot(plt)
    plt.clf()  # Pulisci la figura per evitare sovrapposizioni
    
    plt.figure(figsize=(14, 8))
    sns.stripplot(data=filtered_df, x='Stock', y='Z-Score', hue='Value Generation', palette='viridis', dodge=True)
    plt.xticks(rotation=90)
    plt.title('Distribution of Z-Score by Stock')
    plt.xlabel('Stock')
    plt.ylabel('Z-Score')
    plt.legend(title='Value Generation', loc='upper right')
    plt.tight_layout()
    plt.show()

    # Bar Plot per F-Score
    st.subheader('F-Score by Stock')
    plt.figure(figsize=(14, 8))
    sns.barplot(data=filtered_df, x='Stock', y='F-Score', hue='Value Generation', palette='coolwarm')
    plt.xticks(rotation=90)
    plt.title('F-Score by Stock')
    st.pyplot(plt)
    plt.clf()  # Pulisci la figura per evitare sovrapposizioni
    
    # Heatmap per M-Score
    st.subheader('M-Score Heatmap by Stock and Value Generation')
    pivot = filtered_df.pivot(index='Stock', columns='Value Generation', values='M-Score')
    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot, annot=True, cmap='RdYlGn', center=0)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.title('M-Score Heatmap by Stock and Value Generation')
    st.pyplot(plt)
    plt.clf()  # Pulisci la figura per evitare sovrapposizioni
    
    # Pair Plot per tutte le variabili
    st.subheader('Pair Plot of Key Metrics')
    pair_plot_data = filtered_df[['Fair Value (%)', 'Z-Score', 'F-Score', 'M-Score', 'Value Generation']]
    sns.pairplot(pair_plot_data, hue='Value Generation', palette='viridis')
    st.pyplot(plt)
    plt.clf()  # Pulisci la figura per evitare sovrapposizioni

else:
    st.write("Carica un file CSV per visualizzare i dati e i grafici.")
