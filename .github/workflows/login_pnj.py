import requests

def login_pnj():
    url = "https://www.google.com"
    try:
        response = requests.get(url, timeout=10)

        print("Status code:", response.status_code)

        if response.status_code == 200:
            print("TEST PASSED: Google is reachable")
        else:
            print("TEST FAILED: Unexpected status code")

    except Exception as e:
        print("TEST FAILED:", str(e))


if __name__ == "__main__":
    print("Starting Google test...")
    login_pnj()
    print("Finished.")
