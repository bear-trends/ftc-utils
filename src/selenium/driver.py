from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def start_driver(cfg):
    """Starts webdriver, as hidden and light as possible

    Args:
        cfg (dict): Dict containing config for the webdriver

    Returns:
        [selenium.webdriver.Chrome]: chrome selenium puppet
    """
    options = ChromeOptions()

    # Set ubuntu updated chrome user-agent
    user_agent = cfg["user_agent"]
    options.add_argument(f"user-agent={user_agent}")

    # headless if possible
    if cfg.get("headless"):
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

    if cfg.get("disable_images"):
        options.add_argument("--disable-dev-shm-usage")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
    # Remove webdriver flag
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Disable the automation bar (?)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Disable automation extention
    options.add_experimental_option("useAutomationExtension", False)

    # Chromedriver can be recognized by window size
    options.add_argument("start-maximized")

    # Start driver
    driver = webdriver.Chrome(executable_path=cfg["executable_path"], options=options)

    return driver