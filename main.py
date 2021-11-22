"""Searches for particular script manager methods in Swordie-like script folders

This simple Python script crawls through the files inside the specified 
repository.
It creates a txt file with the name of the method in the output folder.
"""
import os  # standard library

import config
import logger  # local module (Spirit Logger)


spirit_logger = logger.get_logger("main")
spirit_logger.info("Spirit Logger successfully loaded!")
# configuration check:
if not config.REPOSITORY_ROOT:
    spirit_logger.error("Target repository location unknown!")
    spirit_logger.error("Please set the target repository path in config.py!")
    logger.shutdown_logger()
    sys.exit("SpiritMS Script Spider has been terminated.")
# Set folder paths
input_dir = os.path.join(config.REPOSITORY_ROOT, "scripts")
output_dir = os.path.join(os.getcwd(), "output")
spirit_logger.debug(
    f"    Input directory: {input_dir}\n    Output directory: {output_dir}"
)
# sanity check:
if not (os.path.exists(input_dir) and os.path.exists(output_dir)):
    spirit_logger.error("I/O folders do not exist! Please check your files!")
    logger.shutdown_logger()
    sys.exit("SpiritMS Script Spider has been terminated.")


def read_contents(file_path):
    """
    Wrapper for in-built file open

    Args:
        file_path: String, representing the file path
    Returns:
        List of Strings, representing file contents.
        Each element in the list is a line in the file
    """
    spirit_logger.debug(f"    Reading the contents of: {file_path}")
    try:
        with open(file_path, mode="r", encoding="utf-8") as current_file:
            file_contents = current_file.readlines()
    except:
        spirit_logger.warning(
            f"      File is NOT UTF-8! Flagging file: {file_path}"
        )
        file_contents = [
                "[WARNING]",
                "This file is not UTF-8 encoding.",
                "This might be a sign that the encoding is broken,",
                "or that the author had attempted to mix encoding via faulty",
                "copy-paste actions.",
                "This should not be the case for Swordie-based sources.",
                "*PLEASE CHECK THROUGH ITS CONTENTS MANUALLY*",
            ]
    if not file_contents:
        spirit_logger.warning(f"    Could not process: {file_path}")
    return file_contents


def contains_keywords(keyword, line):
    """
    Checks if a string contains the desired keywords. If so, return True.
    Else, return False.
    
    Args:
        String
        
    Returns:
        Boolean
    """
    if keyword in line:
        return True
    return False


def process_file(keywords, file_contents):
    """
    Processes a list of strings, to determine whether they contain the desired
    keywords. If so, append them to an output list.

    Args:
        List of strings
    Returns:
    	List of strings
    """
    output_list = []  # buffer
    # Unparseable files:
    if not file_contents:  # empty files
        spirit_logger.debug("    Unparseable file without encoding errors skipped")
        return output_list
    if file_contents[0] == "[WARNING]":  # Handle files with broken encoding
        output_list = file_contents
        return output_list
        
    # Parseable files:
    last_line_number = len(file_contents) - 1
    count = 1  # number of search results
    pointer = 0  # used to skip the for-loop forward
    for index, line in enumerate(file_contents):
        # Skip forward after finding a keyword found
        if index < pointer:
            continue
        
        # Check if there are non-ASCII characters
        if contains_keywords(keywords, line):
            spirit_logger.debug("Match detected!")
            spirit_logger.debug(f"Number of elements: {len(file_contents)}")
            output_list.append("")
            output_list.append(f"---------- Usage [{count}] at line {index}: ----------")
            output_list.append(line)
            offset = 1
            while True:  # copy all the lines after that, until an empty line
                spirit_logger.debug(f"Line {index+offset}: {file_contents[index+offset]}")
                
                if (not file_contents[index+offset]) or (index + offset == last_line_number):
                    pointer = index + offset + 1
                    break
                output_list.append(file_contents[index+offset])
                offset += 1  # simulate a do-while
    output_list.insert(0, f"Total usages found: {count}")
    spirit_logger.debug(f"    Processed contents: {output_list}")
    return output_list


def write_out(file_name, output_list):
    """
    Takes in the file name (with extension), and uses it to form the output
    path. Then write out the file contents to the output file.

    Args:
        file_name: String, representing the file name and extension
        output_list: List of Strings, representing file contents to write out
    """
    output_path = os.path.join(output_dir, file_name)
    
    spirit_logger.debug(f"    Writing out to: {output_path}")
    # spirit_logger.debug("    Contents to write:")
    # spirit_logger.debug('\n'.join(output_list))
    # No need for try-catch because it will only be UTF-8:
    with open(output_path, mode="w", encoding="utf-8") as output_file:
        output_file.write("".join(output_list))
    return


# Credits: https://stackoverflow.com/questions/18394147/how-to-do-a-recursive-sub-folder-search-and-return-files-in-a-list/59803793#59803793
# Recursive fetching of all files and folders
def run_fast_scandir(dir):    # dir: str
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() == ".py":
                files.append(f.path)


    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files


# Main sequence:
print("===== SpiritMS Script Spider =====")
print("Usage example: To find all usages of ScriptManagerImpl::getNX in scripts")
print("    simply input: getNX")
keyword = input("What is the name of the method you would like to search for? ")
file_name = keyword + ".txt"
keyword = "sm." + keyword + "("
spirit_logger.debug("Start getting files and folders from repository...")
_, file_paths = run_fast_scandir(input_dir)
files = {file: file.replace(input_dir, "")[1:-3] for file in file_paths}


spirit_logger.debug("Now processing files...")
output_buffer = []
for file_path, file_identifier in files.items():
    file_contents = read_contents(file_path)
    output_list = process_file(keyword, file_contents)
    if output_list:
        # if output_list is not empty
        output_buffer.append(f"Usage found in: {file_identifier}")
        output_buffer.extend(output_list)
    spirit_logger.info(f"  Finished processing file: {file_identifier}")
write_out(file_name, output_buffer)
spirit_logger.info("Sequence completed!")
