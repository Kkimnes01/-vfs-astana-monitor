import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

VFS_URL = "https://visa.vfsglobal.com/kaz/en/ita/application-detail"

NO_SLOTS_TEXT = "We are sorry but no appointment slots are currently available"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=30,
    )

    response.raise_for_status()


def check_vfs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1440, "height": 1000},
            locale="en-US",
        )

        print("Opening VFS...")
        page.goto(VFS_URL, wait_until="domcontentloaded", timeout=60000)

        page.wait_for_timeout(8000)

        text = page.locator("body").inner_text()

        print("Page loaded.")
        print(text[:5000])

        if NO_SLOTS_TEXT in text:
            print("❌ No appointments available.")
            browser.close()
            return False

        print("⚠️ The usual 'no slots' message was not found.")
        print("This may mean that a slot is available OR VFS changed the page.")

        browser.close()
        return True


if __name__ == "__main__":
    slot_available = check_vfs()

    if slot_available:
        send_telegram(
            "🚨 ВОЗМОЖНО ПОЯВИЛСЯ СЛОТ НА АСТАНУ! 🇮🇹\n\n"
            "D Visa Study → Enrollment at Universities\n\n"
            "Проверь VFS прямо сейчас:\n"
            f"{VFS_URL}"
        )
