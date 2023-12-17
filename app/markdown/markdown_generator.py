from config import data_dir


class MarkdownGenerator:
    @classmethod
    def generate(cls, grouped_errors: dict, raw_contract: str):
        markdown = cls._generate_markdown(grouped_errors, raw_contract)
        cls._save_markdown(markdown)

    @classmethod
    def _generate_markdown(cls, grouped_erros: dict, raw_contract: str) -> str:
        markdown = ""
        markdown += cls._generate_contract_code(raw_contract)
        markdown += cls._generate_grouped_errors_table(grouped_erros)
        return markdown

    @classmethod
    def _generate_contract_code(cls, contract_code: str):
        markdown = "## Contract\n"
        markdown += f"```solidity\n {contract_code} \n ```\n\n"
        return markdown

    @classmethod
    def _generate_grouped_errors_table(cls, grouped_errors: dict):
        markdown = ""
        markdown += cls._generate_grouped_errors_table_headers()
        markdown += cls._generate_grouped_errors_table_content(grouped_errors);
        return markdown

    @classmethod
    def _generate_grouped_errors_table_headers(cls):
        markdown = "| Error | Securify | Solhint | Slither | Smart Check |\n"
        markdown += "| --- | --- | --- | --- | --- |\n"
        return markdown

    @classmethod
    def _generate_grouped_errors_table_content(cls, grouped_errors: dict):
        markdown = ""
        for error, frameworks in grouped_errors.items():
            securify = "&check;" if "securify" in frameworks else ""
            solhint = "&check;" if "solhint" in frameworks else ""
            slither = "&check;" if "slither" in frameworks else ""
            smartcheck = "&check;" if "smartcheck" in frameworks else ""
            markdown += f"| {error} | {securify} | {solhint} | {slither} | {smartcheck}|\n"
        return markdown

    @classmethod
    def _save_markdown(cls, markdown: str):
        with open(data_dir('report.md'), 'w') as f:
            f.write(markdown)
