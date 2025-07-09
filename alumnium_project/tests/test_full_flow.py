import os
import pytest
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alumnium import Alumni
from browser_use import Agent

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not OPENAI_API_KEY or not GOOGLE_API_KEY:
    raise Exception("Missing OPENAI_API_KEY or GOOGLE_API_KEY in .env file")


@pytest.fixture(scope="function")
def alumni_session():
    print("Opening Chrome...")
    chrome_options = Options()
    driver = Chrome(options=chrome_options)

    print("Loading test page...")
    driver.get("https://todomvc.com/examples/vue/dist/#/")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "new-todo"))
    )

    print("Creating Alumni object...")
    al = Alumni(driver)
    yield al
    print("Closing Chrome...")
    driver.quit()


@pytest.mark.asyncio
async def test_full_flow(alumni_session: Alumni):
    al = alumni_session

    print("Adding first task...")
    al.do("Add a task: 'pick up the kids'")

    print("Adding second task...")
    al.do("Add a task: 'buy milk'")

    print("Marking all tasks complete...")
    al.do("mark all tasks complete using 'Toggle All' button")

    print("Checking if 'buy milk' is completed...")
    al.check("task 'buy milk' is completed")

    print("Starting browser-use agent to delete the task...")
    agent = Agent(task="Delete the task 'buy milk' from the list", llm=None)
    history = await agent.run()
    print("Agent history:\n", history)

    print("Verifying deletion of 'buy milk'...")
    al.check("task 'buy milk' is not in the list")

    print("Test finished successfully.")
