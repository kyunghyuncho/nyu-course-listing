import json

def filter_course_descriptions(input_filename, output_filename):
    """
    Reads a JSON file of courses, removes the 'description' field from each,
    and saves the result to a new JSON file.

    Args:
        input_filename (str): The name of the source JSON file (e.g., 'nyu_courses.json').
        output_filename (str): The name of the destination JSON file.
    """
    try:
        # Open and load the existing JSON file
        with open(input_filename, 'r', encoding='utf-8') as f:
            courses_with_descriptions = json.load(f)
        
        print(f"Successfully loaded {len(courses_with_descriptions)} courses from '{input_filename}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        print("Please make sure the file exists in the same directory as this script.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file '{input_filename}' is not a valid JSON file.")
        return

    # Create a new list of courses, keeping only 'id' and 'title'
    courses_without_descriptions = []
    for course in courses_with_descriptions:
        # Check if 'id' and 'title' exist before adding
        if 'id' in course and 'title' in course:
            courses_without_descriptions.append({
                'id': course['id'],
                'title': course['title']
            })

    # Save the new list to the output file
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(courses_without_descriptions, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully created '{output_filename}' with {len(courses_without_descriptions)} courses.")

    except IOError as e:
        print(f"Error writing to file '{output_filename}': {e}")


if __name__ == '__main__':
    # Define the input and output filenames
    source_file = 'nyu_courses.json'
    destination_file = 'nyu_courses_no_description.json'
    
    # Run the filtering function
    filter_course_descriptions(source_file, destination_file)