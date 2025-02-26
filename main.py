import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Glacier Outreach")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-49969")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()  # Load the portfolio
            jobs = llm.extract_jobs(data)  # Extract job data
        except Exception as e:  # Catch any exceptions during the process
            st.error(f"An error occurred: {e}")
            return  # Exit the function if there's an error

        for job in jobs:
            skills = job.get('skills', [])
            links = portfolio.query_links(skills)  # Query portfolio links based on skills
            email = llm.write_mail(job, links)  # Generate the email
            st.code(email, language='markdown')  # Display the email as markdown

if __name__ == "__main__":
    chain = Chain()  # Initialize the Chain
    portfolio = Portfolio()  # Initialize the Portfolio
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="")
    create_streamlit_app(chain, portfolio, clean_text)  # Run the Streamlit app
