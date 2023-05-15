import GPT

if __name__ == '__main__':
    URL = 'https://vnexpress.net/tin-tuc-24h'
    N = int(input('Input number of content page: '))
    language = input('Language want to translate to: ')
    GPT.Webpage_Translation(N, URL, language)
