import argparse

from chatGPT import Query


class Menu:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-c', '--contract', help='Contract .sol file path')
        self.parser.add_argument('-v', '--version', help='Solidity version')
        self.parser.add_argument('-l', '--lang', help='Output language for the chatbot', default='en')
        self.parser.add_argument('--gpt-version', help='GPT version', default='gpt-3.5-turbo')
        self.parser.add_argument('--tokens', help='Max tokens', default=2048)

    def run(self, runnable):
        args = self.parser.parse_args()
        lang = Query.Lang.create_from(args.lang)

        if not args.contract:
            print("Invalid arguments: use --contract to  specify contract file path")
            exit(1)
        elif not args.version:
            print("Invalid arguments: use --version to specify Solidity version")
            exit(1)

        runnable(args.contract, args.version, lang, args.gpt_version, int(args.tokens))
