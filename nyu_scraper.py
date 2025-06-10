import requests
from bs4 import BeautifulSoup
import json # Import the JSON library
from tqdm import tqdm # Import tqdm for progress bars

def scrape_nyu_courses(url):
    """
    Scrapes all course information from the NYU Course Bulletins website.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the main URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    base_url = "https://bulletins.nyu.edu"
    course_links = []
    
    for link in soup.select('div.az_sitemap ul li a'):
        if link['href'].startswith('/'):
            course_links.append(f"{base_url}{link['href']}")

    all_courses = []
    for link in tqdm(course_links):
        try:
            page_response = requests.get(link)
            page_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"  -> Error fetching {link}: {e}")
            continue

        page_soup = BeautifulSoup(page_response.content, 'html.parser')
        
        for course_block in page_soup.select('div.courseblock'):
            course_id_element = course_block.select_one('span.detail-code strong')
            course_title_element = course_block.select_one('span.detail-title strong')
            course_desc_element = course_block.select_one('div.courseblockextra')

            if course_id_element and course_title_element and course_desc_element:
                all_courses.append({
                    'id': course_id_element.get_text(strip=True),
                    'title': course_title_element.get_text(strip=True),
                    'description': course_desc_element.get_text(strip=True),
                })
            else:
                 print(f"  -> Could not find all details for a course on {link}")

    return all_courses

def save_to_json(courses, filename="nyu_courses.json"):
    """
    Saves the scraped course data to a JSON file.

    Args:
        courses: A list of course dictionaries.
        filename: The name of the output JSON file.
    """
    if not courses:
        print("No courses were scraped to save.")
        return

    with open(filename, 'w', encoding='utf-8') as f:
        # json.dump writes the list of dictionaries to the file
        # indent=4 makes the file human-readable
        # ensure_ascii=False ensures proper handling of special characters
        json.dump(courses, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main_url = "https://bulletins.nyu.edu/courses/"
    scraped_courses = scrape_nyu_courses(main_url)
    if scraped_courses:
        save_to_json(scraped_courses)
        print(f"\nScraping complete. Scraped {len(scraped_courses)} courses and saved to nyu_courses.json")