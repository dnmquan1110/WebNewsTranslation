# Webpage News Translation using GPT
In this kernel, I will crawl new contents from [vnexpress.net/tin-tuc-24h](https://vnexpress.net/tin-tuc-24h) by using Selenium. and use OpenAI API to get engine for translating. After all, the translated content will be output as pdf format.

# Installation Requirement
To run this kernel, you must do the following tasks:
1. Install Selenium WebDriver for crawling content
2. Install pdfkit for export html to pdf
3. Download wkhtmltopdf to use pdfkit
4. Sign up account of OpenAI and get API to using engine


# Running kernel
Using console to run **main.py**. Program require input **N** for the number of contents wanted to crawl, and the name of language wanted to translate from Vietnamese
