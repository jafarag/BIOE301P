# HW1

Dataset Basics & HDF5 Conversion

## Goals

The goals of this homework assignment are to:
1. Describe the details of an approved/chosen dataset for this homework.
2. Convert your chosen dataset to HDF5 format. This will be done with h5py.
3. Access the HDF5 data from Colab and perform a simple visualization.
4. Fine tune HDF5 chunking parameters.

As before, homework must be completed in [Markdown](https://docs.gitlab.com/ee/user/markdown.html), pushed to your private class GitLab repository, rendered to PDF by printing the view of the markdown file from the web browser view of the repository file, and then saved back into the repository. An anonymized zip file of the repository (including markdown, HW PDF, code, any other work files, and excluding the .git directory) is to be submitted for peer grading.

This homework page may be updated later with more details. I recommend not simply forking the repository via the GitLab UI. To hone your skills, it is advised to clone this repository directly in the command line, and then set up a second remote within your subgroup which you push your changes to. This will allow you to practice pulling changes from the originating repository and continuing to push changes to your private repository.

Just a reminder, datasets must be placed in `SCRATCH` which is `/farmshare/scratch/users/<SUNetID>` as home directories can easily get full.

## Questions

1. Demonstrate that both origin and private user repository remotes have been configured for this homework assignment.
    - This is the output of `git remote -v`
    - Remember to maintain anonymity and use `<SUNetID>` instead of your actual SUNetID.
2. Basics
    1. What is the dataset name?
    2. How was it collected? Describe instruments, experiments, subjects, etc.
    3. Where did it come from?
    4. If public, what is the URL to the dataset?
    5. Is there a paper associated with this dataset? Provide the link if so.
    6. Provide a short description of the dataset.
3. File Format
    1. What file format is the data distributed in? Provide a few sentence description of this file format.
    3. Provide an overview of the metadata associated with this dataset.
4. Structure & Encoding
    1. What is the structure of the dataset? Describe the dimensions, organization, hierarchies, etc. Be reasonably detailed so that a reader could reconstruct the structure of the dataset. If there are multiple data structures in the dataset, describe each one.
    2. What is the data encoding model of the dataset? Be descriptive enough so that the explanation goes down to level of the three primitive data classes (integers, characters, and floating-point numbers). 
5. Size
    1. What is the size of the dataset as distributed?
    2. Is the dataset distributed with compression? If so, what compression is used and what is the uncompressed size of the dataset?
    3. Approximate the uncompressed size of the dataset using your understanding of the dataset structure and the encoding model.
        - The math here must be at the level of the three primitive data classes.
        - Provide a web screenshot or console text snippet (use `du` with the appropriate flags for calculating size of a directory, `-sch` or `-scbh` may be helpful here) of the size of the distributed dataset
        - If compression is used, also show the uncompressed dataset size, as that is what is being estimated
        - Video and audio files can be compressed without being put in zip/gzip files, be careful!
    4. Describe any discrepancies between the size of the distributed dataset and the approximate uncompressed data size that you estimated.
6. Workup
    1. What type of analysis could you perform with this data?
    2. Describe potential summary statistics or measures that may be appropriate to calculate.
    3. What types of visualizations might you create with this data?
    4. Why is your chosen dataset well-suited for analysis in HDF5 format?
7. Upload
    1. Place a copy of your dataset in your FarmShare user scratch space: `/farmshare/scratch/users/<SUNetID>`
        - This path is available via the [environment variable](https://en.wikipedia.org/wiki/Environment_variable) `SCRATCH` if the 301P bash_profile is sourced from `/farmshare/home/classes/bioe/301p/bash_profile`.
        - This process could involve `rsync` push from your local system, `wget` pull from the web, or some other mechanism.
    2. Use rclone to copy this dataset from FarmShare to your Google Drive.
    3. Use rclone to copy this dataset from FarmShare to your Google Storage bucket.
8. Convert your dataset to HDF5 format using h5py. Ensure it is chunked, compressed, and uses scaleoffset (if applicable). Be sure to write your code to use paths relative to the `SCRATCH` environment variable. Include this code in your repository and name it `convertH5.py`.
	1. Justify the organization and number of datasets created.
	2. Justify the shape and data type of each dataset.
	3. Compare the storage size of the raw dataset to the HDF5 dataset. Is there a space savings to using HDF5? Why or why not?
9. Upload the HDF5 converted dataset to your Google Drive & Google Storage bucket using rclone.
10. Colab visualization
    1. Use the [colab_sshfs](https://pypi.org/project/colab-sshfs) Python package to mount FarmShare on Google Colab. [FarmShare-specific instructions](https://code.stanford.edu/bil_share/colab_sshfs_sherlock)
    2. Perform some visualization on your HDF5 data (e.g., plot with matplotlib).
        - Access your data by [defining the environment variable](https://stackoverflow.com/questions/5971312/how-to-set-environment-variables-in-python) of `SCRATCH` using `os.environ` to your FarmShare user scratch directory relative to your Colab sshfs mount point.
        - [os.path.join](https://docs.python.org/3/library/os.path.html#os.path.join) is a [very useful function](https://www.geeksforgeeks.org/python-os-path-join-method/) to help with file path generation.
    3. Save this visualization as an image in PNG format (SVG may not work) and include it in your homework repository and [link to it in your markdown](https://about.gitlab.com/handbook/markdown-guide/#images).
    4. Perform the same visualization, but from your Google Drive (no need to save the png).
        - This involves clicking on the folder icon on the left of Colab (tool tip reads: `Files`), and then clicking the directory icon that has a tool tip of `Mount Drive`.
        - You should not alter any of your visualization code for this. You should only need to change the value of your `SCRATCH` environment variable.
    5. Bonus challenge (optional, not graded)
        - Perform the same visualization, but mount your Google Storage Bucket (hint: use gcsfuse).
11. Chunk shape tuning
	1. Describe a simple analysis to perform that will touch a significant fraction (>30%) of the dataset and explain what it will reveal.
		- This can be as simple as performing summary statistics (min, max, mean, median, std deviation, quartiles, etc) on the dataset if no other analysis comes to mind.
	2. Time the duration of this simple analysis on three to five different chunk shapes. All chunk shapes chosen here should either be "along-the-grain" or grainless. Do not choose a chunk shape here that is "against the grain".
		- This can be done with the `timeit` or `time` python modules
        - It is ok if one choice results in very long times. Simply stating it took more than 10x longer than another more sensible chunk shape choice is ok, it does not need to run to completion.
	3. Is there an ideal chunk shape (or chunk shape range) of the dataset for the analysis conducted? If so, what is it and why is it ideal? If not, why not?
12. Perform the same simple analysis as in the prior question but this time use a chunk shape that would result in "cutting against the grain". Compare the timing of this analysis with the timing for the best-performing chunk shape in the prior question.
    - It is ok to stop this early if this takes >10x longer than the more sensible chunk shape approach.
13. Perform the same simple analysis using the originally distributed dataset as the source and compare the timing performance with the prior two questions.
    - It is ok to stop if this takes >10x longer than a sensible chunk shape approach.
14. Bonus challenge (optional, not graded)
    - Play around with [HDF5 chunk caching](https://docs.h5py.org/en/stable/high/file.html#chunk-cache) and various read/write workflows to understand how caching parameters alter I/O speed.
