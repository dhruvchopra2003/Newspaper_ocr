from bs4 import BeautifulSoup
import html
import re


def b_soup(text_article):
    # Create an HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Article</title>
    </head>
    <body>
        <h1>Article Title</h1>
        <p>{text_article}</p>
    </body>
    </html>
    """

    # Parse the HTML template
    soup = BeautifulSoup(html_template, "html.parser")

    # Pretty-print the HTML
    pretty_html = soup.prettify()

    # Save the HTML to a file
    with open("article_template.html", "w", encoding="utf-8") as file:
        file.write(pretty_html)

    print("HTML template created and saved.")


def create_html(headline, article, html_path):
    article = re.sub(r"\n\n", "<br><br>", article)
    article = re.sub(r"    ", "&nbsp", article)
    article = re.sub(r"'", "&apos", article)
    article = re.sub(r'"', "&quot", article)
    # article = html.escape(article)

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{html_path.split()[:-2]}</title>
    </head>
    <body>
        <h1>{headline}</h1>
        <hr>
        <p>{article}</p>
    </body>
    </html>
    """

    # Parse the HTML template
    soup = BeautifulSoup(html_template, "html.parser")

    # Pretty-print the HTML
    pretty_html = soup.prettify()

    with open(html_path, "w") as f:
        f.write(pretty_html)

    print("Saved as HTML")
