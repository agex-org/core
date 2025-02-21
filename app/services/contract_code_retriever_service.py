import json

import requests
from langchain_openai import ChatOpenAI


class ContractCodeRetriever:
    def __init__(self, api_url: str, api_key: str, llm: ChatOpenAI):
        self.api_url = api_url
        self.api_key = api_key
        self.llm = llm

    def get_contract_code(self, address: str) -> dict:
        """Retrieves contract source code from Sonicscan API"""
        try:
            print(f"Retrieving contract source code for address: {address}...")
            url = self.api_url
            params = {
                "module": "contract",
                "action": "getsourcecode",
                "address": address,
                "apikey": self.api_key,
            }

            print("Requesting contract code...")
            response = requests.get(url, params=params)
            print("Contract code requested...")
            data = response.json()

            if data["status"] == "1" and data["result"]:
                source_code = data["result"][0]
                if source_code["SourceCode"] == "":
                    return "Contract source code not verified on Sonicscan"
                raw_source_code = source_code["SourceCode"]
                cleaned_str = raw_source_code[1:-1]
                sources = json.loads(cleaned_str)
                sources = sources.get("sources", {})

                # Create a dictionary to store contract names and their source code
                contracts_dict = {}
                for path, content in sources.items():
                    contracts_dict[path] = content["content"]

                print(f"Retrieved {len(contracts_dict)} contracts.")
                return contracts_dict
            else:
                message = f"Error retrieving source code: {data.get('message', 'Unknown error')}"
                print(message)
                return message
        except Exception as e:
            message = f"Error retrieving contract code: {str(e)}"
            print(message)
            return message

    def get_main_contract_code(self, address: str) -> str:
        """Retrieves the main contract source code from all contract files"""
        contracts_dict = self.get_contract_code(address)

        if isinstance(contracts_dict, str):  # Error message
            return contracts_dict

        print("Getting main contract code...")
        # If there's only one contract, return it
        if len(contracts_dict) == 1:
            print("Only one contract found and returning it...")
            return list(contracts_dict.values())[0]

        # Ask LLM to identify the main contract
        contract_paths = "\n".join(contracts_dict.keys())
        prompt = f"""Given these Solidity contract file paths, identify the main contract file path. 
        Consider that:
        - The main contract often has the same name as the project
        - It's usually not a library or interface
        - It's typically not in a 'lib' or 'interfaces' folder
        - Return ONLY the exact file path, with no formatting, quotes, backticks, or markdown
        - The response should be a single line containing just the path
        
        File paths:
        {contract_paths}"""

        print(f"Prompting LLM to identify main contract path: {prompt}")
        # Get response and clean it up
        main_contract_path = self.llm.invoke(prompt).content.strip()
        print(f"LLM response: {main_contract_path}")
        # Remove any markdown code block formatting, backticks, or extra whitespace
        main_contract_path = main_contract_path.replace("```", "").strip()
        if "\n" in main_contract_path:
            # If multiple lines, take the first non-empty line
            main_contract_path = [
                line.strip() for line in main_contract_path.split("\n") if line.strip()
            ][0]
        print(f"Main contract path after cleanup: {main_contract_path}")

        if main_contract_path in contracts_dict:
            print(f"Main contract path found in contracts_dict: {main_contract_path}")
            return contracts_dict[main_contract_path]
        else:
            message = f"Main contract path not found. Available contracts: {contracts_dict.keys()}"
            print(message)
            return message
