from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv


def create_llm():
    load_dotenv()
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.5,
        max_retries=2,
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    return llm

# Define your desired data structure.


class tenPoints(BaseModel):
    point_1: str = Field(description="Recommendation one of transaction data")
    point_2: str = Field(description="Recommendation two of transaction data")
    point_3: str = Field(description="Recommendation three of transaction data")
    point_4: str = Field(description="Recommendation four of transaction data")
    point_5: str = Field(description="Recommendation five of transaction data")
    point_6: str = Field(description="Recommendation six of transaction data")
    point_7: str = Field(description="Recommendation seven of transaction data")
    point_8: str = Field(description="Recommendation eight of transaction data")
    point_9: str = Field(description="Recommendation nine of transaction data")
    point_10: str = Field(description="Recommendation ten of transaction data")


def invoke_llm(data, llm):
    parser = JsonOutputParser(pydantic_object=tenPoints)

    prompt = PromptTemplate(
        template='''
        Answer the user query based on the provided format instructions and transaction data,
        {format_instructions}
        {data}
        
        Pretend you are a financial advisor, and you have been given data with the following schema:
        - userId: a unique identifier for the user who made the transaction, you can ignore
        - transactionDate: the date of the transaction
        - transactionSubtotal: the subtotal of the transaction
        - transactionItems: the total amount of items
        - transactionTaxes: the total taxes
        - transactionCategory: the category of the purchase
        - transactionPayment: the method of payment
        Make ten points of recommendations based on the data, each point should be a recommendation based on the data
        and be around 5 sentences long, be as detailed as possible and refer to legitimate data for each point.
        
        ''',
        input_variables=["data"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    response = chain.invoke({"data": data})

    return response
