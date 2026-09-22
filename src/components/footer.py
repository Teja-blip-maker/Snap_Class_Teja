import streamlit as st
def footer_home():
    #st.header('Snap class') #By default it takes <h2> tag.
    
    st.markdown(f"""
            <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center;">
            <p style = "font-weight:bold; color:white;">Created with ❤️ by 
            <span style="
                    color:#FF8C00;
                    font-weight:900;
                    font-size:22px;
                    text-shadow:0 0 8px #FFB347;
                ">
                    Teja
                </span></p>
            </div>
                """,unsafe_allow_html=True)