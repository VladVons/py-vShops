from playwright.async_api import async_playwright
import asyncio


async def download_and_parse_page(url):
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=True)  # headless=True runs the browser in the background
        page = await browser.new_page()
        
        # Navigate to the page
        await page.goto(url)
        
        # Wait for the page to load completely
        await page.wait_for_load_state('networkidle')  # Wait until there are no network requests for at least 500 ms
        
        # Get the full HTML content
        html_content = await page.content()
        
        # Close the browser
        await browser.close()
        
        return html_content

async def main():
    url = 'https://setka.ua/c/noutbuki/noutbuki_1/page-5/'
    html = await download_and_parse_page(url)

    # Save or process the HTML content
    with open('downloaded_page.html', 'w', encoding='utf-8') as file:
        file.write(html)

# Run the asynchronous main function
asyncio.run(main())