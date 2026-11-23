import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_scores_service(application_url):
    browser = None
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        browser = webdriver.Chrome(options=options)
        browser.set_page_load_timeout(15)
        browser.get(application_url)

        score_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "score"))
        )
        score_text = score_element.text.strip()
        if not score_text or any(c not in "0123456789" for c in score_text):
            print(f"FAIL: Invalid score value: {score_text!r}")
            return False
        score = int(score_text)
        if not 1 <= score <= 1000:
            print(f"FAIL: Score {score} is outside the range 1-1000.")
            return False
        print(f"PASS: Score is {score}.")
        return True
    except Exception as error:
        print(f"FAIL: {error}")
        return False
    finally:
        if browser is not None:
            try:
                browser.quit()
            except Exception as error:
                print(f"FAIL: Could not close browser: {error}")


def main_function():
    application_url = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.environ.get("APPLICATION_URL", "http://localhost:8777")
    )
    sys.exit(0 if test_scores_service(application_url) else -1)


if __name__ == "__main__":
    main_function()
