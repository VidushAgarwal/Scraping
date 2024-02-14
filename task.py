import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://hprera.nic.in/PublicDashboard"  
driver = webdriver.Chrome()  

driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-6')))


#Here I have given 30s pause because website was loading slowly at time of testing, it can be reduced or modified as per need
time.sleep(30)
projects = driver.find_elements(By.CLASS_NAME, 'col-lg-6')

x=[]
y=[]
for i in range(2,7):
    x.append(projects[i].text.splitlines()[1])
    y.append(projects[i].text.splitlines()[0])

final={}
for i in range(5):
    button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//a[text()="{x[i]}"]')))

    button.click()
    time.sleep(2)

    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'table.table-borderless.table-sm.table-responsive-lg.table-striped.font-sm'))
    )

    rows = table.find_elements(By.TAG_NAME, 'tr')

    data = {}
    need=['Name', 'GSTIN No.','PAN No.', 'Permanent Address']
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) == 2:
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            if key not in need:
                continue
            if key=='PAN No.':
                value=value.split()[0]
            data[key] = value
    final[y[i]]=data
    button = driver.find_element(By.CLASS_NAME, 'close')
    button.click()
driver.quit()

for i in final:
    print(i,":")
    for j in final[i]:
        print(j,':', final[i][j])
    print()