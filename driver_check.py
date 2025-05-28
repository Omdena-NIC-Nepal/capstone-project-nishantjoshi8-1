from webdriver_manager.chrome import ChromeDriverManager

# Automatically fetch the correct version of ChromeDriver for your installed Chrome
driver_path = ChromeDriverManager().install()

print(f"ChromeDriver installed at: {driver_path}")
