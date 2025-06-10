import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

def scrape_nyu_courses(url):
    """
    Scrapes all course information from the NYU Course Bulletins website.

    Args:
        url: The URL of the main courses page.

    Returns:
        A list of dictionaries, where each dictionary represents a course.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the main URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    course_links = []
    
    # Find all links to individual school course pages
    for link in soup.select('div.az_sitemap ul li a'):
        if link is None or 'href' not in link.attrs:
            continue
        if link['href'].startswith('#'):
            continue
        course_links.append(link['href'])

    all_courses = []
    for link in tqdm(course_links):
        try:
            page_response = requests.get(f"https://bulletins.nyu.edu{link}")
            page_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {link}: {e}")
            continue

        page_soup = BeautifulSoup(page_response.content, 'html.parser')
        
        # Find all course blocks on the subject page
        for course_block in page_soup.select('div.courseblock'):
            # Extract course ID, title, and description using specific class names
            course_id_element = course_block.select_one('span.detail-code strong')
            course_title_element = course_block.select_one('span.detail-title strong')
            course_desc_element = course_block.select_one('div.courseblockextra')

            if course_id_element and course_title_element and course_desc_element:
                course_id = course_id_element.get_text(strip=True)
                course_title = course_title_element.get_text(strip=True)
                course_description = course_desc_element.get_text(strip=True)

                all_courses.append({
                    'id': course_id,
                    'title': course_title,
                    'description': course_description,
                })
            else:
                 print(f"  -> Could not find all details for a course on {link}")

    return all_courses

def save_to_csv(courses, filename="nyu_courses.csv"):
    """
    Saves the scraped course data to a CSV file.

    Args:
        courses: A list of course dictionaries.
        filename: The name of the output CSV file.
    """
    if not courses:
        print("No courses were scraped to save.")
        return

    # Updated fieldnames to include the course 'id'
    fieldnames = ['id', 'title', 'description']
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for course in courses:
            writer.writerow(course)

if __name__ == '__main__':
    main_url = "https://bulletins.nyu.edu/courses/"
    scraped_courses = scrape_nyu_courses(main_url)
    if scraped_courses:
        save_to_csv(scraped_courses)
        print(f"Scraped {len(scraped_courses)} courses and saved to nyu_courses.csv")