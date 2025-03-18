from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def create_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        timeout=None,
        max_retries=2,
        api_key = api_key
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                '''
                You are a helpful assistant that takes in financial data {census_data} 
                and user transaction data {transaction_data}, you will generate a list of 10 recommendations
                for the user based on the data provided.
                
                Imagine you are a financial analyst and you are given two datasets, one dataset of financial data
                taken from a website and one dataset of user transaction data. You will use the financial data to
                generate a list of 10 recommendations for the user based on the data provided. 
                The user data is a list of dictionaries while the financial data is a __.
                
                You will return a dictionary with each key being the point it is and each value being the
                recomendation for that point, each key and string will be a string.
                ''',
            ),
        ]
    )
    chain = prompt | llm

    return chain

llm = create_llm()

def invoke_llm(census_data, transaction_data):
    response = llm.invoke(
        {
            'census_data': census_data,
            'transaction_data': transaction_data
        }
    )
    return response.content