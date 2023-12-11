from concurrent.futures import ProcessPoolExecutor
from analyst import smartcheck_analyst, securify_analyst


def run_concurrently(file_path):
    with ProcessPoolExecutor() as executor:
        future_securify = executor.submit(securify_analyst, file_path)
        future_smartcheck = executor.submit(smartcheck_analyst, file_path)

        result_securify = future_securify.result()
        result_smartcheck = future_smartcheck.result()

        print("Securify output:", result_securify)
        print("Smartcheck output:", result_smartcheck)


run_concurrently("../contracts/testContract.sol")
