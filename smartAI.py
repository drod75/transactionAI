"""
Module for generating financial recommendations using LangChain and Google's Gemini model.
Provides functions to create an LLM instance and invoke it with transaction data.
"""
import os
from typing import Dict, Any, List

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class FinancialRecommendations(BaseModel):
    """Structured output format for financial recommendations."""
    point_1: str = Field(description="First recommendation based on transaction data")
    point_2: str = Field(description="Second recommendation based on transaction data")
    point_3: str = Field(description="Third recommendation based on transaction data")
    point_4: str = Field(description="Fourth recommendation based on transaction data")
    point_5: str = Field(description="Fifth recommendation based on transaction data")
    point_6: str = Field(description="Sixth recommendation based on transaction data")
    point_7: str = Field(description="Seventh recommendation based on transaction data")
    point_8: str = Field(description="Eighth recommendation based on transaction data")
    point_9: str = Field(description="Ninth recommendation based on transaction data")
    point_10: str = Field(description="Tenth recommendation based on transaction data")


# Template for financial advice generation
FINANCIAL_ADVICE_TEMPLATE = '''
Answer the user query based on the provided format instructions and transaction data,
{format_instructions}
{data}

Pretend you are a financial advisor, and you have been given data with the following schema:
- transactionId: a unique identifier for the transaction, you can ignore
- userId: a unique identifier for the user who made the transaction, you can ignore
- transactionDate: the date of the transaction  
- transactionSubtotal: the subtotal of the transaction
- transactionItems: the total amount of items
- transactionTaxes: the total taxes
- transactionCategory: the category of the purchase
- transactionPayment: the method of payment

Make ten points of recommendations based on the data, each point should be a recommendation based on the data
and be around a paragraph long, be as detailed as possible and refer to legitimate data for each point.

When I refer to a paragraph I mean a block of seven sentences each containing a minimum of 15 words, you are required
to have at least one paragraph for each point.
'''


def create_llm() -> ChatGoogleGenerativeAI:
    """
    Create and configure a Google Gemini LLM instance.
    
    Returns:
        ChatGoogleGenerativeAI: Configured LLM instance
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.5,
        max_retries=2,
        api_key=api_key,
    )


def invoke_llm(data: List[Dict[str, Any]], llm: ChatGoogleGenerativeAI) -> Dict[str, str]:
    """
    Generate financial recommendations based on transaction data.
    
    Args:
        data: List of transaction records
        llm: LLM instance to use for generation
        
    Returns:
        Dict containing ten financial recommendations
    """
    parser = JsonOutputParser(pydantic_object=FinancialRecommendations)
    
    prompt = PromptTemplate(
        template=FINANCIAL_ADVICE_TEMPLATE,
        input_variables=["data"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    return chain.invoke({"data": data})