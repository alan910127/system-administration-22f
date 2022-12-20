import sys

import requests


def main(base_url: str):
    secret_key = requests.post(
        f"{base_url}/json", json={"keyword": "give_me_secret_key"}
    )

    with open("/home/judge/secret-key.log", "w") as file:
        print(f"secret_key={secret_key.text}", file=file)

    secret_file = requests.post(
        f"{base_url}/urlencoded",
        data={"secretKey": secret_key.json()["secretKey"]},
    )

    with open("/home/judge/secret-file.log", "wb") as file:
        file.write(secret_file.content)

    requests.post(
        f"{base_url}/multipart",
        files={"secretFile": secret_file.content},
    )


if __name__ == "__main__":
    main(sys.argv[1])
