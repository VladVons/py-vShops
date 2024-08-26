class TOlx():
    def __init__(self):
        Opt = Options()
        Opt.add_argument('--headless')
        service = Service('/snap/bin/firefox.geckodriver')
        self.driver = webdriver.Firefox(service=service, options=Opt)

    def GetProducts(self, aUrl: str) -> list:
        print(aUrl)
        self.driver.get(aUrl)

        PageReady = 2
        time.sleep(PageReady)
        Sleep = random.randint(1, 3)
        time.sleep(Sleep)

        WebDriverWait(self.driver, 10).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, ".css-bc4qtv"))
         )

        Res = []
        products = self.driver.find_elements(By.CSS_SELECTOR, ".css-1grlwc9")
        pass
        for product in products:
            Name = product.find_element(By.CSS_SELECTOR, "p.css-ki4ei7 a").text
            Price = product.find_element(By.CSS_SELECTOR, "span[data-testid='ad-price']").text
            Price = Price.replace('грн.', '').replace(' ', '')
            Url = product.find_element(By.CSS_SELECTOR, "p.css-ki4ei7 a").get_attribute('href')
            Res.append([Name, Price, Url])
        return Res

