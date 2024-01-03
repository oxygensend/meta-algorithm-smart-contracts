import subprocess
from concurrent.futures import ProcessPoolExecutor

from dotenv import load_dotenv

from analyst import smartcheck_analyst, securify_analyst, solhint_analyst, slither_analyst
from markdown import MarkdownGenerator
from config import delete_data_dir
from chatGPT import ChatGPT, Query
from menu import Menu
import logging


def run_concurrently(file_path):
    with ProcessPoolExecutor() as executor:
        future_securify = executor.submit(securify_analyst, file_path)
        future_smartcheck = executor.submit(smartcheck_analyst, file_path)
        future_solhint = executor.submit(solhint_analyst, file_path)
        future_slither = executor.submit(slither_analyst, file_path)

        result_securify = future_securify.result()
        result_smartcheck = future_smartcheck.result()
        result_solhint = future_solhint.result()
        result_slither = future_slither.result()

        print("Securify output:", result_securify[0])
        print("Smartcheck output:", result_smartcheck[0])
        print("Solhint output:", result_solhint[0])
        print("Slither output:", result_slither[0])
        return result_securify[0], result_smartcheck[0], result_solhint[0], result_slither[1]


def run(file_path, version, lang, gpt_version, tokens):
    changeSolidityVersion(version)

    if validate_contract(file_path):
        result_securify, result_smartcheck, result_solhint, result_slither = run_concurrently(file_path)
    else:
        print("Invalid contract file")
        exit(-4)

    print("Running with arguments:")
    print("Contract file path:", file_path)
    print("Solidity version:", version)
    print("Output language:", lang)
    print("GPT version:", gpt_version)
    print("Tokens:", tokens)

    chat = ChatGPT(gpt_version, tokens)
    grouped_errors = group_errors(chat, result_securify, result_solhint, result_slither, result_smartcheck)
    print(grouped_errors)
    with open(file_path, 'r') as f:
        raw_contract = f.read()

    suggs = suggestions(chat, raw_contract, result_securify, result_solhint, result_slither, result_smartcheck)
    print(suggs)

    MarkdownGenerator.generate(grouped_errors, raw_contract, suggs)


def group_errors(chat, securify, solhint, slither, smartcheck):
    question = Query.GENERATE_TABLE.builder(securify, solhint, slither, smartcheck)
    result = chat.ask_gpt(question)
    logging.info(f"Chatbot response: {result}")
    return eval(result)


def suggestions(chat, code, securify, solhint, slither, smartcheck):
    errors = securify + '\n' + solhint + '\n' + slither + '\n' + smartcheck
    question = Query.SUGGESTIONS.builder_suggestions(code, errors)
    result = chat.ask_gpt(question)
    logging.info(f"Chatbot response: {result}")
    return eval(result)


def changeSolidityVersion(version):
    try:
        # Install and use the specified version
        install_command = f'solc-select install {version}'
        use_command = f'solc-select use {version}'

        subprocess.run(install_command, shell=True, check=True)
        subprocess.run(use_command, shell=True, check=True)

        logging.info(f"Solidity version changed to {version} successfully!")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to change Solidity version. Error: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False


def validate_contract(file_path):
    try:
        command = f'solc {file_path} --combined-json abi,bin'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            logging.info(f"Contract compiled successfully!")
            return True
        else:
            logging.error(f"Contract compilation failed with errors: {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Invalid contract file: {e}")
        return False


if __name__ == '__main__':
    # run_concurrently("../contracts/testContract.sol")
    load_dotenv()
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    delete_data_dir()

    Menu().run(run)
