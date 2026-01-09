
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture console logs
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))

        # Load the local HTML file
        cwd = os.getcwd()
        file_path = f"file://{cwd}/index.html"
        print(f"Loading {file_path}")
        page.goto(file_path)

        # 3. Enter Hub
        print("Entering Hub...")
        page.evaluate("startHubPhase()")
        page.wait_for_selector(".hub-menu")

        # Check if function exists
        exists = page.evaluate("typeof window.startWorkshopPhase === 'function'")
        print(f"startWorkshopPhase exists: {exists}")

        # 4. Check Workshop Screen
        print("Checking Workshop...")

        # Click Hub Item
        # Force click just in case
        page.locator(".hub-card").filter(has_text="Atölye").click(force=True)

        # Wait for transition
        page.wait_for_timeout(1000)

        h2 = page.locator("h2").text_content()
        print(f"Current H2: '{h2}'")

        if "ATÖLYE" not in h2:
             print("FAILED: Did not enter Workshop.")
             # Check if we can call it manually
             print("Attempting manual call...")
             page.evaluate("startWorkshopPhase()")
             page.wait_for_timeout(500)
             h2_after = page.locator("h2").text_content()
             print(f"H2 after manual call: '{h2_after}'")
        else:
             print("SUCCESS: Entered Workshop")

        page.screenshot(path="verification/step5_workshop.png")

        browser.close()

if __name__ == "__main__":
    run()
