"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--mode", "-m", required=True,
                        choices=["validate", "complete"])
    parser.add_argument("postcode")

    args = parser.parse_args()

    mode = args.mode
    postcode = args.postcode.upper().strip()

    if mode == "validate":
        is_valid = validate_postcode(postcode)
        if not is_valid:
            print(f"{postcode} is not a valid postcode.")
        else:
            print(f'{postcode} is a valid postcode.')

    else:
        try:
            completions = get_postcode_completions(postcode)
        except ValueError:
            print(f"No matches for {postcode}.")

        for i in range(5):
            print(completions[i])
