import os

# LOOPING THROUGH DIRECTORY TO GRAB FILE PATH
# Searches for a file with the specified filename in the specified directory
# and its subdirectories. Returns the complete file path if the file is found,
# or None if the file is not found.
def find_file(filename, directory):
    for root, dirs, files in os.walk(directory):
        # os.walk() generates the directory tree recursively.
        # It returns three values on each iteration: the current directory path (root),
        # a list of subdirectories in the current directory (dirs),
        # and a list of files in the current directory (files).
        for file in files:
            # Check each file in the current directory for a match with the specified filename.
            if file == filename:
                # If a match is found, construct the complete file path using os.path.join()
                # and return it.
                return os.path.join(root, file)
    
    # If the function reaches this point, the file was not found in the directory tree.
    # Return None to indicate that the file was not found.
    return None


def read_file(filename):
    # Set the size of each chunk to read from the file.
    CHUNK_SIZE = 5242880

    # Open the file in binary mode for reading.
    with open(filename, 'rb') as _file:
        # Loop until we reach the end of the file.
        while True:
            # Read the next chunk of data from the file.
            data = _file.read(CHUNK_SIZE)
            # If there is no more data to read, break out of the loop.
            if not data:
                break
            # Yield the current chunk of data, allowing the caller to process it.
            yield data