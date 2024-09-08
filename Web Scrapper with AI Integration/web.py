import requests
from bs4 import BeautifulSoup
import openai
import os

# Set your OpenAI API key here
# Ideally, use environment variables to keep this secure
openai.api_key = 'g.a000nQgKmdnx0eXDb7lzrzcODUFPf2vnQSl0WtLb0_KbrxmaLANWb7UF3vxD5-D1PUuiziYXpAACgYKAcESARISFQHGX2MiujSzOdU2msKV2_zl-6FBrRoVAUF8yKrno2rY-X8axJ2wS7VjXNff0076'  # Replace with your actual API key

def fetch_headings_and_paragraphs(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize a list to store headings and paragraphs
    content = []

    # Find all headings and paragraphs
    for heading_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for heading in soup.find_all(heading_tag):
            content.append({'type': 'heading', 'text': heading.get_text(strip=True)})

    for paragraph in soup.find_all('p'):
        content.append({'type': 'paragraph', 'text': paragraph.get_text(strip=True)})
    
    return content

def summarize_text(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following text:\n\n{text}",
            max_tokens=150
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return text

def generate_additional_info(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Provide additional information or context related to the following text:\n\n{text}",
            max_tokens=150
        )
        additional_info = response.choices[0].text.strip()
        return additional_info
    except Exception as e:
        print(f"Error generating additional information: {e}")
        return "No additional information available."

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in content:
            if item['type'] == 'heading':
                file.write(f"**{item['text']}**\n")
            elif item['type'] == 'paragraph':
                file.write(f"\nParagraph: {item['text']}\n")
                summary = summarize_text(item['text'])
                file.write(f"Summary: {summary}\n")
                additional_info = generate_additional_info(item['text'])
                file.write(f"Additional Information: {additional_info}\n")
                file.write("\n" + "-"*80 + "\n")

def main():
    # URL of the website you want to scrape
    url = 'https://www.geeksforgeeks.org/java-basic-syntax/?ref=lbp'  # Replace with the URL you want to scrape
    print("Fetching headings and paragraphs from the webpage...")
    content = fetch_headings_and_paragraphs(url)
    
    if content:
        print("Saving content to file...")
        save_to_file(content, 'headings_paragraphs_and_summaries.txt')
        print("Content saved to headings_paragraphs_and_summaries.txt")
    else:
        print("No content found or failed to fetch content.")

if __name__ == '__main__':
    main()
