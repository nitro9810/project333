from solana.account import Account
from solana.rpc.api import Client
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from base64 import b64encode
import json

# Solana RPC endpoint (testnet for example)
solana_url = "https://api.devnet.solana.com"
client = Client(solana_url)

# Wallet setup
wallet = Account()

# Mint token function (dummy function, replace with your actual minting logic)
def mint_nft(wallet, recipient_address, contract_address, token_metadata):
    # Convert the token metadata to bytes
    metadata_bytes = json.dumps(token_metadata).encode("utf-8")

    # Create a mint transaction
    mint_transaction = Transaction()
    mint_transaction.add(
        TransactionInstruction(
            program_id=contract_address,
            data=metadata_bytes,
            keys=[
                AccountMeta(pubkey=wallet.public_key(), is_signer=True, is_writable=False),
                AccountMeta(pubkey=recipient_address, is_signer=False, is_writable=True),
            ],
        )
    )

    # Sign and submit the transaction
    result = client.send_transaction(mint_transaction, wallet)
    return result

if __name__ == "__main__":
    # Obtain user input for the recipient's Solana address, smart contract address, and other data
    recipient_address = input("Enter the recipient's Solana address: ")
    contract_address = input("Enter the smart contract address: ")
    token_name = input("Enter the name of the NFT: ")
    token_symbol = input("Enter the symbol of the NFT: ")
    image_file_path = input("Enter the path to the image file: ")

    # Create token metadata
    token_metadata = {
        "name": token_name,
        "symbol": token_symbol,
    }

    # Read image data and encode it in base64
    with open(image_file_path, "rb") as image_file:
        image_data = b64encode(image_file.read()).decode("utf-8")

    # Include image data in the token metadata
    token_metadata["image"] = f"data:image/png;base64,{image_data}"

    # Mint the NFT
    mint_result = mint_nft(wallet, recipient_address, contract_address, token_metadata)

    # Display the transaction result
    print("Transaction result:", mint_result["result"])
    print("Transaction ID:", mint_result["result"]["txid"])
