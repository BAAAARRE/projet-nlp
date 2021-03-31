import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import plotly_express as px
import plotly.graph_objects as go
import stylecloud

def main():

# Set configs
    st.set_page_config(
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	page_title='Projet NLP',  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
    )

# Set Sidebar
    st.sidebar.title('Navigation onglet')
    page = st.sidebar.selectbox("Choisir une page", ["Global", "Détails"])

# Load data
    df_topics = pd.read_csv('topics.csv')
    df_content = pd.read_csv('content_topics.csv')
    df_top_words = pd.read_csv('top_words.csv')
    df_graph = pd.read_csv('df_graph.csv')
    score = [0.7418812993631643, 0.8769720266857137, 0.9090304143932807, 0.8794974370954498, 0.869526364036107, 0.9141504537335862, 0.9189604469027266, 0.9117102227158748, 0.8758614076691177, 0.8397482197631981]

### Page global ###
    if page == 'Global':
# pyLDAvis
        st.title('pyLDAvis')
        HtmlFile = open("gsdmm_html.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, width= 1800, height = 800)

# Distribution du nombre de propositions par sujets
        st.title('Distribution du nombre de propositions par sujets')
        fig = px.bar(df_topics, x='nb_sents', y='topic_name', text = 'nb_sents', orientation='h')
        fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
        st.write(fig)

# MDS
        st.write('\n')
        st.title('Graphique')
        mds = go.Figure(data=[go.Scatter(
        x= df_graph['x'],
        y= df_graph['y'],
        mode='markers + text',
        text = df_topics['topic_name'],
        textposition="top center",
        marker=dict(
            color= score,
            size=df_graph['Freq']*3,
            colorbar=dict(
                title="Score"
            ),
                colorscale="Bluered"
            )
            )])
        annote_graph(mds, "Agir individuellement", 0, 0.5)
        annote_graph(mds, "Agir collectivement", 1, 0.6)
        annote_graph(mds, "Autour de la nourriture", 0.5, 1)
        annote_graph(mds, "Nourriture", 0.5, 0)
        mds.update_layout(height=900, width=900, xaxis_range=[-0.36,0.35], yaxis_range=[-0.35,0.35])
        st.write(mds)

# Résultats Make.org
        st.title('Résultats Make.org')
        st.image('Rapport.png')

### Page détails ###
    if page == 'Détails':
# Choisissez un sujet
        st.write('\n')
        st.title('Choisissez un sujet :')
        sel_topic = st.selectbox('', sorted(df_topics['topic_name'].unique()))
        df_topic_select =  df_topics[df_topics['topic_name'] == sel_topic]
        df_content_select =  df_content[df_content['topic_name'] == sel_topic]
        df_top_words_select =  df_top_words[df_top_words['topic_name'] == sel_topic]
        st.title('Définition :')
        st.write(list(df_topic_select['def'])[0])

# Mots les plus fréquents
        st.title('Mots les plus fréquents')
        fig2 = px.bar(df_top_words_select, x='freq', y='word', text = 'freq', orientation='h')
        fig2.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
        fig2.update_layout( width=870, height=870)
        st.write(fig2)

# Nuage de mots
        st.write('\n')
        st.title('Nuage de mots')
        max_cld = st.number_input('Nombre de mots dans le nuage', format="%i", value=100)
        wrd_cld(df_content_select, max_cld)
        st.write('\n')
        st.image('stylecloud.png')

# Propositions
        st.write('\n')
        my_expander = st.beta_expander('Exemple de proposition')
        with my_expander:
            for i in df_content_select["proposition"]:
                st.write(i)

# Bottom page
    st.write("\n") 
    st.write("\n")
    st.info("""Data Source : [Make.org](https://make.org/FR)""")


### Functions ###
def wrd_cld(dataframe, max):
    texte = dataframe.clean.str.cat(sep=' ')
    stylecloud.gen_stylecloud(text = texte,
                          icon_name='fas fa-apple-alt',
                          #palette='colorbrewer.diverging.Spectral_11',
                          background_color='white',
                          gradient='horizontal',
                          max_words = max
                         ) 

def annote_graph(figu, text, x, y):
        figu.add_annotation(text=text,
                  xref="paper", yref="paper",
                  x=x, y=y, showarrow=False,
                  font=dict(
                    family="Trebuchet MS",
                    size=18,
                    color="#CB0E1A"
            ))

if __name__ == "__main__":
    main()
