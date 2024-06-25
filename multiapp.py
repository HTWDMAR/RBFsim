"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        st.sidebar.title(":red[Pages]")
        #st.sidebar.markdown("---")
        app = st.sidebar.radio(
        #app = st.sidebar.selectbox(
            '',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()
        with st.sidebar:
            st.markdown("""<p class="fund_txt">Funded by: German Federal Ministry of Education and Research<br>(BMBF Grant Nr. 02WME1612)<br>MEWAC programme<br>"Feasibility of Managed Aquifer Recharge for Safe and Sustainable Water Supply" (FEMAR) Project</p>""", unsafe_allow_html=True)
            log1, log2 = st.columns(2)
            with log1:
                st.image('images/BMBF.jpg')
            with log2:
                st.image('images/MEWAC_logo.jpeg')
            st.markdown("""<style>
                p.fund_txt{
                    font-size : 0.8rem;
                    font-style : italic;
                }
                div[data-testid="stHorizontalBlock"]{
                    gap : 0.3rem;
                    align-items : center
                }
            </style>""", unsafe_allow_html=True)
            st.divider()
