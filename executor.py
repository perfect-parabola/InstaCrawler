from ChromeCrawler.Crawler import ChromeInstaCrawler

username = "your instagram username"
password = "your instagram password"
query = "query you want to search"
max_count = "max count of image you want to download"

driver = ChromeInstaCrawler()
driver.execute(username, password, query, max_count)