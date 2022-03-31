"""
This file is the framework for generating multiple Streamlit applications 
through an object oriented framework. 
"""

# Import necessary libraries 
import streamlit as st
# st.markdown(
#             f'''
#             <style>
#                 .reportview-container .sidebar-content {{
#                     padding-top: {0}rem;
#                 }}
#                 .reportview-container .main .block-container {{
#                     padding-top: {0}rem;
#                 }}
#             </style>
#             ''',unsafe_allow_html=True)


# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        """Class Method to Add pages to the project

        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.pages.append(
            {
                "title": title, 
                "function": func
            }
        )

    def run(self):
        # Drodown to select the page to run  
        # col1,col2 ,col3=st.columns(3)
        # page = col1.selectbox(
        #     'Navigation Bar', 
        #     self.pages, 
        #     format_func=lambda page: page['title']
        # )

        page = st.radio("",self.pages,format_func=lambda page: page['title'])
 
        # st.button("Single Image",on_click=self.pages[0]['function'])

        if 'red' not in st.session_state:
            st.session_state['red'] = 2.20
            st.session_state['green']=10.00
            st.session_state['blue']=10.00
            st.session_state["disk_radius"]=15



        # if col3.button("Reset Settings"):
        #     st.session_state['red'] = 0.5
        #     st.session_state['green']=8.0
        #     st.session_state['blue']=8.0
        #     st.session_state["disk_radius"]=15
            

        # run the app function 
        page['function']()
        # print(page['function'])
        # print(self.pages)



