from typing import Final

from langchain import chat_models

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


def check_for_correctness(problem: list[str]) -> bool:
    """Explain the error in a problem

    Args:
        problem (str): problem statement

    Returns:
        str: explanation of error
    """
    problem = "\n".join(problem)
    print(f"check_for_correctness: {problem}")
    context = f"Is there a mistake with the maths? Answer with yes or no only. (Don't worry about the latex itself, just the maths.) Also, if there's not enough context don't worry: {problem!r}"
    response = get_chat_model().call_as_llm(context, max_tokens=1) 
    print(f"check_for_correctness: {response}")
    return response.lower() == "no"

def explain_error(problem: list[str]) -> str:
    """Explain the error in a problem

    Args:
        problem (str): problem statement

    Returns:
        str: explanation of error
    """
    problem = "\n".join(problem)
    context = f"The following is not correct: {problem!r}, explain why it is wrong."
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
