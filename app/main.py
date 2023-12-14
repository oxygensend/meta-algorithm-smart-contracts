import subprocess
from concurrent.futures import ProcessPoolExecutor
from analyst import smartcheck_analyst, securify_analyst, solhint_analyst, slither_analyst
from chatGPT import ChatGPT, Query
from menu import Menu
import logging


def run_concurrently(file_path):
    with ProcessPoolExecutor() as executor:
        future_securify = executor.submit(securify_analyst, file_path)
        future_smartcheck = executor.submit(smartcheck_analyst, file_path)
        future_solhint = executor.submit(solhint_analyst, file_path)
        future_slither = executor.submit(slither_analyst, file_path)

        result_securify = future_securify.result(),
        result_smartcheck = future_smartcheck.result(),
        result_solhint = future_solhint.result(),
        result_slither = future_slither.result(),

        print("Securify output:", result_securify)
        print("Smartcheck output:", result_smartcheck)
        print("Solhint output:", result_solhint)
        print("Slither output:", result_slither)
        return result_securify, result_smartcheck, result_solhint, result_slither


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
    question = Query.GENERATE_TABLE.builder(result_securify, result_solhint, result_slither, result_smartcheck)
    print(question)
    result = chat.ask_gpt(question)
    print(result)


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
    Menu().run(run)
