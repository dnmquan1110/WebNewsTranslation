import openai
from tqdm import tqdm
import CrawlContent

openai.api_key = "YOUR-API-KEY"

def model_response(to_translate: str,  language: str, max_token):
    response = openai.Completion.create(
        model="text-curie-001",
        prompt="Translate this to " + language + "\n" + to_translate,
        temperature=0.3,
        max_tokens=max_token,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text

def translate(content, language: str):
    new_title = model_response(content.title, language, 1024)
    new_description = model_response(content.description, language, 1024)
    new_contents = [model_response(c, language, 1024) for c in content.content]
    new_date = model_response(content.date, language, 10)
    new_author = model_response(content.author, language, 10)
    return CrawlContent.Content(new_date, new_title, new_description, new_contents, new_author)

def Webpage_Translation(N: int, url: str, translate_language: str):
    list_content_link = []
    url = url
    page = 1
    while len(list_content_link) < N:
        content_link, url = CrawlContent.get_content_link(url, page)
        list_content_link.extend(content_link)
        page += 1
    list_content_link = list_content_link[:N]
    list_content = []
    for i in tqdm(range(len(list_content_link)), desc='Get content of each link and translate to ' + translate_language):
        c = CrawlContent.get_content_of_each_link(list_content_link[i])
        if c is not None:
            list_content.append(translate(c, translate_language))

    for i in tqdm(range(len(list_content)), desc= "Export to pdf: "):
        CrawlContent.export_to_pdf(list_content[i], i + 1)