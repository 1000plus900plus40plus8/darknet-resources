import os
import random
from pathlib import Path


def get_files_from_folder(folder: str) -> [Path]:
    # get all the files recursively in the folder using glob
    # https://docs.python.org/3/library/glob.html
    # https://docs.python.org/3/library/pathlib.html
    files = [f for f in Path(folder).glob('**/*') if f.is_file()]
    # return the files using absolute paths
    return [f.absolute() for f in files]


def filter_valid_files(files):
    # filter out the files that are used for training and have been validated by DarkMark
    image_file_extensions = ['.jpg', '.jpeg', '.png']
    training_file_extensions = ['.txt', '.json']
    # group the files by their path stem
    files_by_stem = {}
    for file_by_stem in files:
        stem = Path(file_by_stem).stem
        if stem not in files_by_stem:
            files_by_stem[stem] = []
        files_by_stem[stem].append(file_by_stem)
    # filter out the files that are not used for training
    valid_files = {}
    for file_by_stem in files_by_stem:
        files_using_stem = files_by_stem[file_by_stem]
        if len(files_using_stem) == 1:
            # if there is only one file for a stem, then it is NOT used for training
            continue
        # get the file extensions for our files_for_stem list
        file_extensions = [Path(filepath).suffix for filepath in files_using_stem]

        has_images = any(e in image_file_extensions for e in file_extensions)
        has_training_files = all(
            e in file_extensions for e in training_file_extensions)
        files_used_in_training = has_images and has_training_files

        if not files_used_in_training:
            continue

        directory_and_file_name = os.path.join(os.path.dirname(files_using_stem[0]), file_by_stem)
        if directory_and_file_name not in valid_files:
            valid_files[directory_and_file_name] = []
        valid_files[directory_and_file_name].append(files_using_stem)
    return valid_files


def get_fraction_of_dataset(directory_to_search: str, directory_to_copy_to: str, fraction: float):
    # clear the folder if it exists
    print(f'Clearing folder: {directory_to_copy_to}')
    if os.path.exists(directory_to_copy_to):
        os.system('rm -rf ' + directory_to_copy_to)
    os.system('mkdir ' + directory_to_copy_to)
    print('Getting files from folder: ' + directory_to_search)
    # get all the files in the folder
    files = get_files_from_folder(directory_to_search)
    print(f'Found {len(files)} files in {directory_to_search}')
    # filter out the files that are used for training and have been validated by DarkMark
    valid_files = filter_valid_files(files)
    valid_files_keys = list(valid_files.keys())
    print(f'Found {len(valid_files_keys)} valid files')
    # group valid files by their directory
    valid_files_by_directory = {}
    for file_by_stem in valid_files_keys:
        directory = Path(file_by_stem).parent
        if directory not in valid_files_by_directory:
            valid_files_by_directory[directory] = []
        valid_files_by_directory[directory].append(file_by_stem)
    print(f'Found {len(valid_files_by_directory)} valid files by directory')
    fraction_of_directories = {}
    # get a fraction of the files in each directory
    for directory in valid_files_by_directory:
        files_for_directory = valid_files_by_directory[directory]
        num_files_to_copy = int(len(files_for_directory) * fraction)
        files_to_copy = random.sample(files_for_directory, num_files_to_copy)
        fraction_of_directories[directory] = files_to_copy
    print(
        f'Found {len(fraction_of_directories)} directories with fraction of files')
    total_files_copied = 0
    # copy the files to the new folder
    for directory in fraction_of_directories:
        file_stems_to_copy = fraction_of_directories[directory]
        files_copied_from_directory = 0

        nested_folder_to_copy_to = os.path.join(
            directory_to_copy_to, os.path.basename(directory))

        # make the directory if it does not exist
        if not os.path.exists(nested_folder_to_copy_to):
            os.system('mkdir ' + nested_folder_to_copy_to)

        for file_stem_to_copy in file_stems_to_copy:
            for files_to_copy in valid_files[file_stem_to_copy]:
                for file_to_copy in files_to_copy:
                    file_to_copy_to = os.path.join(
                        nested_folder_to_copy_to, os.path.basename(file_to_copy))

                    os.system(f'cp {file_to_copy} {file_to_copy_to}')
                    files_copied_from_directory += 1
        print(
            f'Copied {files_copied_from_directory} files to {nested_folder_to_copy_to}')
        total_files_copied += files_copied_from_directory
    print(f'Copied {total_files_copied} files to {directory_to_copy_to}')


if __name__ == "__main__":
    # define the folder we will copy to
    directory_to_copy_to = './'

    # define the folder we will search for the images
    directory_to_search = 'training_data'

    fraction = 0.1
    get_fraction_of_dataset(directory_to_search, directory_to_copy_to, fraction)
