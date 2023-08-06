from typing import Final

from langchain import chat_models
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TYPES: Final[list[str]] = [
    "Algebra",
    "Simple Arithmetic",
    "Linear Algebra",
]


def get_chat_model() -> chat_models.ChatOpenAI:
    return chat_models.ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.0,
    )


def classify_problem_type(problem: str) -> str:
    """Classify the problem type

    Args:
        problem (str): problem statement

    Returns:
        str: problem type
    """
    context = f"Given this problem: {problem!r} classify the problem type as one of the following: {TYPES}"
    return get_chat_model().call_as_llm(context)


def classify_variable_type(problem: str) -> str:
    pass


def explain_error(problem: str) -> str:
    """Explain the error in a problem

    Args:
        problem (str): problem statement

    Returns:
        str: explanation of error
    """
    context = f"This expression is wrong: {problem!r}, explain why it is wrong"
    return get_chat_model().call_as_llm(context)


def explain_solution(problem: str) -> str:
    """Explain the solution to a problem

    Args:
        problem (str): problem statement

    Returns:
        str: explanation of solution
    """
    context = (
        f"Given this problem: {problem!r}, first show the answer and then show detailed steps on how to get to the "
        "solution"
    )
    return get_chat_model().call_as_llm(context)


def provide_solution(problem: str) -> str:
    context = f"Given this problem: {problem!r}, say whether it is correct or not"
    return get_chat_model().call_as_llm(context)
