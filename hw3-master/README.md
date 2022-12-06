---
title: "22S BioE 301P HW3"
geometry: margin=0.5in
---


# HW3

Slurm & Pipelines

## Goals

The goal of this homework assignment is to work with the slurm job scheduler to build simple pipelines.

As before, homework must be completed in Markdown, pushed to a private GitLab repository, rendered to PDF, and then saved back into the repository. For any question involving code, either include the .py file used answer the question and indicate this filename in the markdown file for that question or directly include the code in the markdown file in a code block section for that question number. A zip file of the repository (including markdown, PDF, any other work files, and excluding the .git directory) must be submitted for peer grading. It's fine to include ipynb files, but if you are doing so, you must also submit validated, working [code blocks](https://python-markdown.github.io/extensions/fenced_code_blocks) for specific questions within your Markdown file with appropriate [syntax highlighting](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks#syntax-highlighting).

This homework page may be updated later with more details. Do not simply fork the repository. Clone this repository directly, and then set up a second remote with which you push your changes to. This will allow you to pull changes from the originating repository and continue to push changes to your private repository. 

## Training

- YouTube Series on [Cluster Computing](https://www.youtube.com/watch?v=zME-Zj4lTLg&list=PLczxDQk890sYdREK2wVRw04DfQJZRZdUU)
- [Slurm Documentation](https://slurm.schedmd.com/documentation.html)
    - [Slurm command summary](https://slurm.schedmd.com/pdfs/summary.pdf)
    - [Slurm dependencies](https://hpc.nih.gov/docs/job_dependencies.html)
- Bash tutorials
    - [LinuxCommand.org](http://linuxcommand.org)
    - [Ryan's Tutorials: Bash scripting](https://ryanstutorials.net/bash-scripting-tutorial/bash-script.php)
- YAML
    - [File Spec](https://yaml.org/spec/1.2.2/#chapter-2-language-overview)
    - [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
    - [PyYAML Tutorial](https://python.land/data-processing/python-yaml)
- Plotly
    - [Plotly Python](https://plotly.com/python)
    - [write_html](https://plotly.github.io/plotly.py-docs/generated/plotly.io.write_html.html)
- HTML
    - [W3 HTML Basics](https://www.w3schools.com/html/html_basic.asp)
    - [Jinja templating](https://jinja.palletsprojects.com/en/3.1.x/templates)
    - [Jinja API](https://jinja.palletsprojects.com/en/3.1.x/api)

## Questions

### 1. Pipelines
In this question, you will be designing a data pipeline in slurm. This pipeline will 1) download raw data, 2) convert it to an appropriate derivative dataset file format, 3) perform some analysis, 4) generate a visualization, and 5) publish the results to the web. This must be completed in FarmShare. I ***strongly recommend*** first playing around with a few simple [toy examples](https://en.wikipedia.org/wiki/Toy_program) that you build to understand how slurm, [srun](https://slurm.schedmd.com/srun.html), and [sbatch](https://slurm.schedmd.com/sbatch.html) work before trying to complete this question. Be sure to check the status of your submitted jobs with [squeue](https://slurm.schedmd.com/squeue.html) and cancel jobs with [scancel](https://slurm.schedmd.com/scancel.html). This assignment cannot be successfully completed without understanding the differences between program execution, singularity-based program execution, and slurm job program execution--this question will utilize and nest all three elements. As you are assembling the pipeline, it is ***strongly recommended*** to first ensure that the stage works independent of slurm with just singularity-based program execution before embedding it in a slurm job.

#### 1. Select a new dataset that is at least 10GB in size (uncompressed).
- This cannot be a dataset you used in a prior homework.
- Choose a dataset that has at least two base items in it (e.g., participants, subjects, distinct data tables, experimental sessions, etc).
- Be sure that the dataset can be programmatically downloaded (via wget, rclone, datalad, etc).
#### 2. Create a bash script called `pipeline.sh` that submits jobs using `sbatch` broken down into five stages.
- The bash script will define two environment variables: `DATA_RAW` and `DATA_DERIV`. Both of these must be defined relative to the `SCRATCH` environment variable.
- Each stage will be [dependent](https://slurm.schedmd.com/sbatch.html#OPT_dependency) on the successful completion of prior ones, so the subsequent jobs in a pipeline will need to wait until the appropriate time to be run.
    - This is performed with the sbatch paramater `-d afterok:<JOBID>` leveraging the [`--parsable`](https://slurm.schedmd.com/sbatch.html#OPT_parsable) flag.
    - An example of how to set dependent jobs is below:
    ```shell
    JOB_ID1=$(sbatch --parsable <other parameters> )
    JOB_ID2=$(sbatch --parsable -d afterok:$JOB_ID1 <other parameters> )
    ```
- Stages:
    1. Download - the first job will downlaod the raw data and place it within `DATA_RAW`.
        - For data sources like BigQuery, this stage can be combined with the convert stage, but pipeline development will likely be slower.
        - It may be helpful to refer to each base item by the environment variable `DATASET_ID` specific for that sbatch call
            - The example code for this appears here:
            ```shell
            JOB_ID1=$(sbatch --export=ALL,DATASET_ID='subject34' --parsable <other parameters> )
            ```
            - The command called by the job will have access to the environemnt variable `DATASET_ID` when it is executed by slurm.
            - Use this construct if helpful for the download or convert stages--it may not be necessary at download or convert stages if the dataset is already packaged with more than one base item. However, this approach is required for the analyze stage.
    2. Convert - the second job will convert it to an appropriate derivative file format (HDF5, SQLite, video, etc), carrying over any relevant metadata, and store this in `DATA_DERIV`.
        - The different base items must be in different directories within `DATA_DERIV`.
        - After this job is complete, it is not permitted to refer back to `DATA_RAW` by any subsequent step in the pipeline, so be sure all relevant data/metadata from `DATA_RAW` necessary to perform the desired analysis is copied forward to `DATA_DERIV` in some intelligent manner.
            - I recommend storing small metadata as a yaml file.
        - A [job array](https://slurm.schedmd.com/job_array.html) may be very helpful at this stage in speeding this data conversion over. Job arrays perform [embarrassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel) operations.
    3. Analyze - the next set of jobs will perform some analysis on the data.
        - Specify at least two jobs to be run (one for each base element), with the unique environemnt variable `DATASET_ID` passed in for each.
        - Each of these jobs must submit a job array that splits up the analysis (either by splitting up the dataset, the operations to perform, or both) in some sensible fashion. This is known as a [scatter](https://en.wikipedia.org/wiki/Collective_operation#Scatter_[9]) operation.
        - The job array environment variables SLURM sets will be key to your Python code knowing what piece of the data to operate on or what action to take.
        - The results of this analysis and scatter operations must be saved down sensibly.
            - One option for this is to save down files within `DATA_DERIV`. One file per job array element is recommended in this case. This could be a yaml file (recommended), a numpy [npy](https://numpy.org/doc/stable/reference/generated/numpy.save.html) or [npz](https://numpy.org/doc/stable/reference/generated/numpy.save.html) file, a pandas [pickle](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html) file, etc.
            - Another option would be to have each job array element upload a row (or mulitple rows) of information into a BigQuery table
        - Once the the job array is complete, the [shards](https://en.wikipedia.org/wiki/Shard_(database_architecture)) need to be collected into a single file in one final sbatch job. This is known as a [gather](https://en.wikipedia.org/wiki/Collective_operation#Gather_[8]) operation.
            - For a scatter operation which wrote individual files in `DATA_DERIV`, the gather operation will open all files and collect the information into a single file.
            - For a scatter operation performed on BigQuery, no such job is necessary as BigQuery automatically gathers all shards.
    4. Visualize - the next job will generate a [plotly](https://plotly.com/python) visualization on the data in the gather step.
        - Use `write_html` to export the plot to HTML and save it sensibly within `DATA_DERIV`
        - Both base elements must be present in the visualization, either as separate plots or as a single plot that combines both base elements.
    5. Publish - the next job will create an HTML file, embed the visualization, and upload it to the web.
        - Add a title, description, brief (no more than a few sentences is needed) writeup of the data source, and caption the plotly figure(s).
        - This will be done with Python jinja templating.
            - This is a bare bones html jinja template that can be used for embedding the visualization, name this `hw3_template.html` (or similar) within a `templates` directory inside your homework repository:
            ```html
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>22S BioE 301P - HW3</title>
            </head>
            <body>
                <h1>22S BioE 30P - HW3</h1>
                <h2>Pipelines</h2>
                <h3>Data source</h3>
                    <p>The data was acquired from...(retain anonymity, do not name a specific lab if you are affiliated with it)</p>
                <h3>Analysis</h3>
                    <p>The analysis performed on this dataset was...</p>
                <h4>Visualization</h4>
                # jinja will insert the contents of the plotly_visualization variable here
                # You will need multiple of these if you have more than one plot
                {{plotly_visualization}}
                <p>Figure 1: ...</p>
            </body>
            </html>
            ```
            - This template can be rendered with the following code:
            ```python
            # code to load plotly visualization html file as a string
            with open("<path to plotly html file>") as f:
                str_viz = f.read()

            # load jinja and render
            from jinja2 import Environment, FileSystemLoader
            env = Environment(loader=FileSystemLoader("<path of templates directory in HW3>"), autoescape=False)
            template = env.get_template("hw3_template.html")
            final_html = template.render(plotly_visualization = str_viz)

            # save renderd HTML
            with open("<path to save rendered html file>", 'w') as f:
                f.write(final_html)
            ```
        - Copy this finished HTML to your Google Drive and Google Storage bucket.
            - This is to be done programmatically in python via the slurm job.
            - Use [python-rclone](https://pypi.org/project/python-rclone) for Google Drive and Google Storage.
            - This code will make your FarmShare rclone config available to the python-rclone library:
            ```python
            import os
            import rclone

            with open(os.path.join(os.path.expanduser('~'), '.config', 'rclone', 'rclone.conf')) as f:
                cfg = f.read()

            rclone.with_config(cfg).copy("<source>", "<dest>")
            ```
        - Copy this HTML to your AFS web space
            - This cannot be done via slurm, must be done manually, and can only be done on rice (or some other system that has AFS)
        - Print an anonymized PDF view of the rendered web page from your AFS web space and include it in your homework submission.

### 2. More Git training: [Learn Git Branching](https://learngitbranching.js.org)
This website presents a set of challenges to learn Git better.
Complete the following modules.
- Main
    - Introduction Sequence
    - Ramping Up
- Remote
    - The first six within "Push & Pull -- Git Remotes" 
Include screenshots, linked from the Markdown, of the both main & remote windows when complete.
