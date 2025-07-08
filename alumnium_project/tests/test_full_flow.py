import os
import pytest
import asyncio
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alumnium import Alumni
from browser_use import Agent


@pytest.fixture(scope="function")
def alumni_session():
    print("Opening Chrome...")
    chrome_options = Options()
    driver = Chrome(options=chrome_options)
    driver.get("https://todomvc.com/examples/vue/dist/#/")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "new-todo"))
    )
    print("Page loaded, creating Alumni...")
    al = Alumni(driver)
    yield al
    print("Closing Chrome...")
    driver.quit()


@pytest.mark.asyncio
async def test_full_flow(alumni_session: Alumni):
    al = alumni_session
    print("Starting Selenium actions via Alumni...")

    print("Adding first task...")
    al.do("Add a task: 'pick up the kids'")
    print("Adding second task...")
    al.do("Add a task: 'buy milk'")
    print("Marking all tasks complete...")
    al.do("mark all tasks complete using 'Toggle All' button")
    print("Checking if 'buy milk' is completed...")
    al.check("task 'buy milk' is completed")

    print("Starting Browser-use agent for simple task...")
    agent = Agent(task="Delete the task 'buy milk' from the list", llm=None)
    history = await agent.run()
    print("Agent run history:")
    print(history)

    print("Checking if 'buy milk' task is deleted...")
    al.check("task 'buy milk' is not in the list")

    print("Test finished successfully.")
