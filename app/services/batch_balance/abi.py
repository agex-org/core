abi = [
    {"stateMutability": "payable", "type": "fallback"},
    {
        "inputs": [
            {"internalType": "address[]", "name": "users", "type": "address[]"},
            {"internalType": "address[]", "name": "tokens", "type": "address[]"},
        ],
        "name": "getAllTokensBalances",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "user", "type": "address"},
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "blockTimestamp",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct BalanceChecker.BalanceInfo[]",
                "name": "",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "user", "type": "address"},
                    {"internalType": "address", "name": "token", "type": "address"},
                ],
                "internalType": "struct BalanceChecker.BalanceRequest[]",
                "name": "requests",
                "type": "tuple[]",
            }
        ],
        "name": "getSelectedTokenBalances",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "user", "type": "address"},
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "balance", "type": "uint256"},
                    {
                        "internalType": "uint256",
                        "name": "blockNumber",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "blockTimestamp",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct BalanceChecker.BalanceInfo[]",
                "name": "",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {"stateMutability": "payable", "type": "receive"},
]
