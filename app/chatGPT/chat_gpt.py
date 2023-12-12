import logging
import threading

import openai
from dotenv import load_dotenv
from openai import RateLimitError
from urllib3.exceptions import ReadTimeoutError

from .prompt import Prompt
import os
import time

load_dotenv()


class ChatGPT:
    CHAT = 'CHAT'

    def __init__(self, version: str = 'gpt3.5-turbo', tokens: int = 2048):
        self.key = os.getenv("OPENAI_API_KEY")
        self.version = version
        self.tokens = tokens

    def ask_gpt(self, question: str, attempt: int = 0):
        try:
            openai.api_key = self.key
            prompt = Prompt(self.version, 0.68, self.tokens, ChatGPT.CHAT, question)
            return self._create_response(prompt)
        except RateLimitError:
            logging.warning(
                f"Thread [{threading.current_thread().name}] Rate limit exceeded, waiting 20 seconds for question {question} and trying again in 3 attempts left {3 - attempt}")
            time.sleep(20)
            if attempt > 3:
                logging.error(
                    f"Thread [{threading.current_thread().name}] Rate limit exceeded for question {question}, tried 3 times, giving up")
                raise Exception("Rate limit exceeded")
            return self.ask_gpt(question, attempt + 1)
        except ReadTimeoutError:
            logging.warning(
                f"Thread [{threading.current_thread().name}] Read timeout exceeded, waiting 20 seconds for question {question} and trying again in 3 attempts left {3 - attempt}")
            time.sleep(20)
            if attempt > 3:
                logging.error(
                    f"Thread [{threading.current_thread().name}] Read timeout exceeded for question {question}, tried 3 times, giving up")
                raise Exception("Read timeout exceeded")
            return self.ask_gpt(question, attempt + 1)

    def _create_response(self, prompt: Prompt):
        message = {'role': 'user', 'content': prompt.prompt}
        return openai.ChatCompletion.create(
            model=prompt.engine,
            temperature=prompt.max_temperature,
            max_tokens=prompt.max_tokens,
            messages=[message]
        )['choices'][0]['message']['content']
