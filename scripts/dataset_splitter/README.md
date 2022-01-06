# Dataset Splitter

**This script assumes you are using DarkMark for working with your training data and as a result expects a JSON file with the same name as your image file and txt file**



The expected structure of the training data is as follows:
(Assuming training-data is in cwd)

```bash
training-data/folder1/image1.jpg
training-data/folder1/image1.txt
training-data/folder1/image1.json
training-data/folder1/image2.jpg
training-data/folder1/image2.txt
training-data/folder1/image2.json

training-data/folder2/image3.jpg
training-data/folder2/image3.txt
training-data/folder2/image3.json
training-data/folder2/image4.jpg
training-data/folder2/image4.txt
training-data/folder2/image4.json

training-data/folder3/image5.jpg
training-data/folder3/image5.txt
training-data/folder3/image5.json
training-data/folder3/image6.jpg
training-data/folder3/image6.txt
training-data/folder3/image6.json
```

Now assuming we want to take 50% (0.50) of our training data we expect the new training dataset to be something like this:

# !!! the split-training-data folder is removed at the start of the program !!!

```bash
split-training-data/folder1/image1.jpg
split-training-data/folder1/image1.txt
split-training-data/folder1/image1.json

split-training-data/folder2/image4.jpg
split-training-data/folder2/image4.txt
split-training-data/folder2/image4.json

split-training-data/folder3/image6.jpg
split-training-data/folder3/image6.txt
split-training-data/folder3/image6.json
```

Files are selection is handled by python random module so your results will vary every time you run this script

# TODO:

- Add tests

- Add argparse for validation and for a flag to not require jsons


