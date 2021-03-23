import streamlit as st
import pandas as pd
import plotly_express as px

import stylecloud

def main():

# Set configs
    st.set_page_config(
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	page_title='Projet NLP',  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
    )

    df_topics = pd.read_csv('topics.csv')
    df_content = pd.read_csv('content_topics.csv')
    df_top_words = pd.read_csv('top_words.csv')

    st.title('Distribution du nombre de propositions par sujets')
    fig = px.bar(df_topics, x='nb_sents', y='topic_name', text = 'nb_sents', orientation='h')
    fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
    st.write(fig)

    st.title('Choisissez un sujet :')
    sel_topic = st.selectbox('', sorted(df_topics['topic_name'].unique()))
    df_topic_select =  df_topics[df_topics['topic_name'] == sel_topic]
    df_content_select =  df_content[df_content['topic_name'] == sel_topic]
    df_top_words_select =  df_top_words[df_top_words['topic_name'] == sel_topic]
    st.title('Définition :')
    st.write(list(df_topic_select['def'])[0])

    st.title('Mots les plus fréquents')
    fig2 = px.bar(df_top_words_select, x='freq', y='word', text = 'freq', orientation='h')
    fig2.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
    fig2.update_layout( width=870, height=870)
    st.write(fig2)

    st.write('\n')
    st.title('Nuage de mots')
    max_cld = st.number_input('Nombre de mots dans le nuage', format="%i", value=100)
    wrd_cld(df_content_select, max_cld)
    st.write('\n')
    st.image('stylecloud.png')

    st.write('\n')
    my_expander = st.beta_expander('Exemple de proposition')
    with my_expander:
        for i in df_content_select["proposition"]:
            st.write(i)



def wrd_cld(dataframe, max):
    texte = dataframe.clean.str.cat(sep=' ')
    stylecloud.gen_stylecloud(text = texte,
                          icon_name='fas fa-apple-alt',
                          #palette='colorbrewer.diverging.Spectral_11',
                          background_color='white',
                          gradient='horizontal',
                          max_words = max
                         ) 


if __name__ == "__main__":
    main()
