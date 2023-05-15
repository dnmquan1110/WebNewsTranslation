from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pdfkit

edge_options = webdriver.EdgeOptions()
edge_options.add_argument('--start-minimized')

class Content:
    def __init__(self, date, title, description, contents, author):
        self.date = date
        self.title = title
        self.description = description
        self.content = contents
        self.author = author

    def printContent(self):
        print(self.date)
        print(self.title)
        print(self.description)
        print(self.content)
        print(self.author)


def get_content_link(url: str, page: int):
    driver = webdriver.Edge('edgedriver.exe', options=edge_options)
    driver.get(url)

    # Set initial empty list for each element:
    content_link = []

    for i in tqdm(range(30), desc='Get content links of page {0}'.format(page)):
        flink = driver.find_element(By.XPATH, "//a[@data-medium='Item-{0}']".format(str(30*(page-1)+i+1))).get_attribute('href')
        content_link.append(flink)

    next_page = driver.find_element(By.XPATH, "//a[@class='btn-page next-page ']").get_attribute('href')
    driver.quit()
    return content_link, next_page

def get_content_of_each_link(url):
    driver = webdriver.Edge('edgedriver.exe')
    driver.get(url)

    date = driver.find_element(By.XPATH, "//span[@class='date']").text
    block = driver.find_element(By.CLASS_NAME, 'sidebar-1')
    try:
        title = block.find_element(By.XPATH, "//h1[@class='title-detail']").text
    except:
        try:
            title = block.find_element(By.XPATH, "//h1[@class='title-detail ']").text
        except:
            title = None

    if title is None:
        return None
    description = block.find_element(By.XPATH, "//p[@class='description']").text
    contents = []
    try:
        fck_detail = block.find_element(By.XPATH, "//article[@class='fck_detail ']")
    except:
        fck_detail = block.find_element(By.XPATH, "//article[@class='fck_detail']")
    normals = fck_detail.find_elements(By.XPATH, "//p[@class='Normal']")
    if len(normals) == 0:
        desc_cation = fck_detail.find_elements(By.XPATH, "//div[@class='desc_cation']")
        for d in desc_cation:
            normals.extend(d.find_elements(By.TAG_NAME, 'p'))
    for n in normals:
        contents.append(n.text)
    return Content(date, title, description, contents[:-1], contents[-1])


def export_to_pdf(content, index):
    html = """
    <html>
    <head>
      <style>
        
        body {
            font-family: Arial, sans-serif;
            margin: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        date {
            float: right;
            color: #757575;
            font-size: 14px;
        }
        h1 {
            text-align: center;
            color: black;
            font-size: 32px;
        }
        p {
            text-align: justify;
            line-height: 1.5;
            font-size: 20px;
        }
        .author {
            text-align: right;
            font-weight: bold;
            font-size: 20px;
        }
      </style>
    </head>
    <body>
        <p class="date">%s</p>
        <div class="container">
            <h1>%s</h1>
            <p>%s</p>
            <p>%s</p>
            <p class="author">%s</p>
            <a class=
        </div>
    </body>
    </html>
    """ % (content.date, content.title, content.description, '</br>'.join(content.content), content.author)

    options = {'encoding': "UTF-8"}
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdfkit.from_string(html, 'content {}.pdf'.format(index), configuration=config, options=options)

