import os
import openai
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class LLM():
    def __init__(self):
        self.types = ["Algebra", "Simple Arithmetic", "Linear Algebra"]

    def classify_problem_type(self, problem:str)->str:
        """Classify the problem type

        Args:
            problem (str): problem statement

        Returns:
            str: problem type
        """
        context=f"Given this problem: \'{problem}\' classify the problem type as one of the following: {str(self.types)}"
        return self._call(context)

    def classify_variable_type(self, problem:str)->str:
        pass

    def explain_error(self,problem:str)->str:
        """Explain the error in a problem

        Args:
            problem (str): problem statement

        Returns:
            str: explanation of error
        """
        context=f"This expression is wrong: \'{problem}\', explain why it is wrong"
        return self._call(context)

    def explain_solution(self, problem:str)->str:
        """Explain the solution to a problem

        Args:
            problem (str): problem statement

        Returns:
            str: explanation of solution
        """
        context=f"Given this problem: \'{problem}\', first show the answer and then show detailed steps on how to get to the solution"
        return self._call(context)

    def provide_solution(self, problem:str)->str:
        context=f"Given this problem: \'{problem}\', say whether it is correct or not"
        return self._call(context)

    def _call(self, content:str)->str:
        """Calling GPT-3 to generate an response

        Args:
            content (str): prompt to GPT

        Returns:
            str: GPT response
        """
        # Load API key from an environment variable
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        message = [
            {"role": "user", "content": content}
        ]
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)
        assert(chat_completion["choices"][0]["finish_reason"] == "stop")
        return chat_completion["choices"][0]["message"]["content"]

