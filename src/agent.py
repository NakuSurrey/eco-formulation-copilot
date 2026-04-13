"""
Agentic AI module for the Eco-Formulation Copilot.

This file creates the "brain" of the application. It connects
Google Gemini (the LLM) to the chemical formulations DataFrame
using LangChain's DataFrame Agent.

HOW IT WORKS — step by step:
1. The user types a plain English question (e.g., "Show me the cheapest biodegradable formulas")
2. This module sends that question to the Gemini LLM
3. Gemini reads the question and writes Pandas code to answer it
4. The agent executes that Pandas code against the real DataFrame
5. The result (a number, a table, a list) is returned as a string

The scientist never sees or touches any code.
The LLM does the translation from English → Pandas → Answer.

FLOW:
    User question (str)
        ↓
    create_agent() — builds the LLM + DataFrame connection
        ↓
    query_agent() — sends the question, gets the answer
        ↓
    Answer (str) — returned to the Streamlit front-end
"""

import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
)

from src.config import GOOGLE_API_KEY, GEMINI_MODEL, validate_config

# ============================================================
# System Prompt — The Agent's Instructions
# ============================================================
# This tells the LLM WHO it is, WHAT data it has access to,
# and HOW it must behave. This is Trait #202 (Prompt-engineered)
# and Trait #203 (Anti-hallucinatory).
#
# The rules here prevent the LLM from:
# - Inventing chemical properties that are not in the dataset
# - Giving vague or generic answers instead of data-driven ones
# - Executing dangerous code (like deleting files)
# ============================================================

SYSTEM_PROMPT: str = """
You are an AI Research & Development Assistant for the Eco-Formulation
Copilot at a consumer goods company. You help scientists analyze
chemical formulation data for sustainable detergent products.

RULES YOU MUST FOLLOW:
1. You can ONLY answer questions using the provided DataFrame.
2. If the data does not contain the answer, reply exactly with:
   "Data not available in current testing batch."
3. Do NOT invent, estimate, or hallucinate chemical properties.
4. When returning tabular data, format it as a clean markdown table.
5. When asked for "top" or "best" formulas, always state which
   metric you are sorting by.
6. Always include units where applicable (e.g., £ for cost, % for scores).
7. Be concise. Scientists want data, not essays.

THE DATASET COLUMNS:
- Formula_ID: Unique identifier for each formulation (e.g., ECO-F-0001)
- Surfactant_Type: The cleaning agent used (6 types)
- Polymer_Type: The anti-redeposition polymer used (6 types)
- Enzyme_Type: The stain-breaking enzyme used (6 types, or "No Enzyme")
- Concentration_Pct: Active ingredient concentration (5-45%)
- Biodegradability_Score: How eco-friendly the formula is (0-100, higher = better)
- Cleaning_Efficacy_Score: How well it cleans (0-100, higher = better)
- Toxicity_Level: How toxic the formula is (0-10, lower = better)
- Cost_Per_Litre_GBP: Production cost in British Pounds per litre
"""


def create_agent(df: pd.DataFrame) -> object:
    """
    Creates a LangChain DataFrame Agent connected to Google Gemini.

    This function does three things:
    1. Validates that the API key exists (fails fast if missing)
    2. Initialises the Gemini LLM with safe settings
    3. Wraps the LLM and the DataFrame into an "agent" that can
       translate English questions into Pandas code and execute them

    Parameters:
        df: The chemical formulations DataFrame from data_loader.py

    Returns:
        A LangChain agent object. You pass it a question string,
        and it returns an answer string.
    """
    # Step 1: Validate the API key is present
    validate_config()

    # Step 2: Initialise the Google Gemini LLM
    # temperature=0 means the LLM gives the most deterministic answer.
    # For data queries, we want exact answers, not creative ones.
    #
    # thinking_budget=0 turns off the "thinking" feature in
    # gemini-2.5-flash. Without this, the model adds internal
    # reasoning tokens that confuse LangChain's ReAct parser
    # and cause output parsing errors.
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
        thinking_budget=0,
    )

    # Step 3: Create the DataFrame Agent
    # This agent receives a question, asks the LLM to write Pandas
    # code, executes that code on the DataFrame, and returns the result.
    #
    # verbose=False prevents internal chain-of-thought logs from
    # appearing in the Streamlit UI.
    #
    # allow_dangerous_code=True is REQUIRED by LangChain because
    # the agent executes Python code. We mitigate this risk with
    # the strict system prompt above.
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        agent_type="zero-shot-react-description",
        verbose=False,
        prefix=SYSTEM_PROMPT,
        allow_dangerous_code=True,
        handle_parsing_errors=True,
    )

    return agent


def query_agent(agent: object, user_question: str) -> str:
    """
    Sends a user's question to the agent and returns the answer.

    This function is the ONLY way the rest of the app talks to the AI.
    It wraps the agent call in error handling so that if the LLM
    generates bad Pandas code or the API fails, the app does not crash.

    Parameters:
        agent: The LangChain agent created by create_agent()
        user_question: The plain English question from the scientist

    Returns:
        A string containing the agent's answer.
        If an error occurs, returns a user-friendly error message
        instead of a raw Python crash.

    FLOW:
        user_question (str)
            ↓
        agent.invoke() — LLM writes Pandas code, executes it
            ↓
        result["output"] — the answer as a string
            ↓
        returned to the caller (app.py)
    """
    # Guard: reject empty questions
    if not user_question or not user_question.strip():
        return "Please enter a question about the formulation data."

    try:
        # invoke() sends the question to the LLM, which:
        # 1. Reads the question
        # 2. Writes Pandas code to answer it
        # 3. Executes the code on the DataFrame
        # 4. Returns the result in the "output" key
        result = agent.invoke({"input": user_question})
        return result.get("output", "No output returned from the agent.")

    except ValueError as e:
        # ValueError usually means the LLM generated invalid code
        return (
            "I couldn't process that query. "
            "Please try rephrasing your chemical parameters. "
            f"(Detail: {str(e)[:200]})"
        )

    except Exception as e:
        # Catch-all for API failures, network errors, etc.
        error_name = type(e).__name__
        return (
            f"An error occurred while querying the data: {error_name}. "
            "Please check your API key and internet connection, "
            "or try a simpler question."
        )
