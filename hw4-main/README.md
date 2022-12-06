---
title: "22S BioE 301P HW4"
geometry: margin=0.5in
---


# HW4

GitLab CI Pipelines & Interactive Dashboards

## Goals

The goal of this homework assignment is to deploy pipelines onto slurm using GitLab and build and deploy interactive dashboards.

As before, homework must be completed in Markdown, pushed to a private GitLab repository, rendered to PDF, and then saved back into the repository. For any question involving code, either include the .py file used answer the question and indicate this filename in the markdown file for that question or directly include the code in the markdown file in a code block section for that question number. A zip file of the repository (including markdown, PDF, any other work files, and excluding the .git directory) must be submitted for peer grading. It's fine to include ipynb files, but if you are doing so, you must also submit validated, working [code blocks](https://python-markdown.github.io/extensions/fenced_code_blocks) for specific questions within your Markdown file with appropriate [syntax highlighting](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks#syntax-highlighting).

This homework page may be updated later with more details. Do not simply fork the repository. Clone this repository directly, and then set up a second remote with which you push your changes to. This will allow you to pull changes from the originating repository and continue to push changes to your private repository. 

## Training

- [Gitlab CI](https://docs.gitlab.com/ee/ci/pipelines)
    - [.gitlab-ci.yml](https://docs.gitlab.com/ee/ci/yaml/gitlab_ci_yaml.html)
    - [gcip](https://dbsystel.gitlab.io/gitlab-ci-python-library/user/index.html) (optional)
    - [GitLab Runners](https://docs.gitlab.com/runner)

- [Bokeh](https://docs.bokeh.org/en/latest/docs/user_guide.html)
    - [Bokeh Tutorial](https://docs.bokeh.org/en/latest/docs/first_steps.html)
    - [Running a Bokeh server](https://docs.bokeh.org/en/latest/docs/user_guide/server.html)

- [Heroku](https://devcenter.heroku.com/categories/reference)
    - [Getting Started with Python](https://devcenter.heroku.com/articles/getting-started-with-python) (at least through the "Define a Procfile" step, the rest are optional)

- Python pip [requirements.txt](https://pip.pypa.io/en/stable/reference/requirements-file-format) file format

## Instructions

This assignment builds upon the prior homework, executing a more sophisticated pipeline and deploying the Python web application to Heroku hosting. The goal is to develop a GitLab CI pipeline (implemented as the HW4 repository), that manages a slurm pipieline (similar to HW3), and outputs a working Bokeh dashboard which is then deployed to Heroku at the end of the pipeline. It is fine to use the same dataset and pipeline as in HW3, or use a different dataset.

This assignment has multiple concepts to learn, which can only then be assembled together.
The concepts and skills to develop, in no specific order, are:
- Deploying a GitLab CI Pipeline onto FarmShare or FarmCloud
- Building an interactive dashboard in Bokeh
- Deploying and hosting a Python application (the Bokeh dashboard) on Heroku

### GitLab CI
GitLab uses runners to deploy pipelines. You must [register a project-specific GitLab runner](https://docs.gitlab.com/ee/ci/runners/runners_scope.html#create-a-specific-runner) for each space you want to deploy pipelines to (FarmShare or FarmCloud). I have already installed the runners with a **custom** executor for slurm on both FarmShare on FarmCloud, but you must register the runner with your repository. I ***strongly recommend*** working on test cases to understand how GitLab CI Pipelines deploy jobs against the runner with toy examples before completing the assignment.

Once registered, edit your `~/.gitlab-runner/config.toml` with the following lines.
Change the first line with `concurrent=1` to have a higher value, like 10 or 20.
Edit the `[runners.custom]` section in the following manner:

For FarmShare:
```
[runners.custom]
  config_exec   = "/farmshare/home/classes/bioe/301p/2108_gitlab_executor_slurm/config.sh"
  prepare_exec  = "/farmshare/home/classes/bioe/301p/2108_gitlab_executor_slurm/prepare.sh"
  run_exec      = "/farmshare/home/classes/bioe/301p/2108_gitlab_executor_slurm/run.sh"
  cleanup_exec  = "/farmshare/home/classes/bioe/301p/2108_gitlab_executor_slurm/cleanup.sh"
```
For FarmCloud:
```
[runners.custom]
  config_exec   = "/barley/2108_gitlab_executor_slurm/config.sh"
  prepare_exec  = "/barley/2108_gitlab_executor_slurm/prepare.sh"
  run_exec      = "/barley/2108_gitlab_executor_slurm/run.sh"
  cleanup_exec  = "/barley/2108_gitlab_executor_slurm/cleanup.sh"
```

Also ensure that `[runners.custom_build_dir]` is enabled:
```
[runners.custom_build_dir]
  enabled = true
```

The GitLab runner needs to be running to accept jobs from the GitLab server. Run `gitlab-runner run` in a persistent tmux window.


A skeleton `.gitlab-ci.yml` file (to be placed in the base directory of your HW repository:
```
variables:
  GIT_CLONE_PATH: $CI_BUILDS_DIR/$CI_CONCURRENT_ID/$CI_PROJECT_PATH

stages: # define the stages for the pipeline
  - download
  - convert
  - analyze

download-dset01:
  stage: download
  variables:
    SCHEDULER_PARAMETERS: "-c 1 --mem 200M -t 5:0"
  tags:
    - FarmCloud
  script:
    - rclone copy aws:<s3 bucket>/dset01 $SCRATCH/RAW/dset01 --transfers 10
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push"'
      when: never
    - when: always
```

### Bokeh
The creation of the Bokeh application will take the place of the `visualization` stage in the pipeline from HW3.
The Bokeh dashboard should have at least one interactive element (slider, dropdown, radio buttons, etc) and at least one plot.

I ***strongly recommend*** first testing Bokeh in standalone mode, running it as a server on FarmShare/FarmCloud using `bokeh serve --show <app.py>`. This will set up a local server on the FarmShare/FarmCloud node. In order to connect to this, an [SSH tunnel](https://goteleport.com/blog/ssh-tunneling-explained) must be made from your local compute to this server process. Generic instructions [here](https://www.concordia.ca/ginacody/aits/support/faq/ssh-tunnel.html).

For FarmShare, this takes the form of:
```
ssh <SUNetID>@riceXX.stanford.edu -N -L <local port>:localhost:<bokeh serve port>
```

For FarmCloud, this takes the form of:
```
gcloud --project=soe-bioe-301p compute ssh farmcloud-login0 -- -N -L <local port>:localhost:<bokeh serve port>
```

### Heroku
After working through the Heroku documentation of `Getting Started with Python` linked in the training, I ***strongly recommend*** working through a toy example with Heroku before trying to integrate it into your pipeline. Try the [sliders demo](https://demo.bokeh.org/sliders) (sliders demo [source code](https://github.com/bokeh/bokeh/blob/master/examples/app/sliders.py)) or any of the other [Bokeh Demos](https://demo.bokeh.org). Initialize a blank repository and deploy one of these demos to Heroku to gain experience with deploying Python applications from scratch.

Register for a free personal account and deploy your Bokeh application on Heroku. Be sure the name of your application is anonymous.

There is no need to install the heroku client. It is available in the singularity container.

The deployment of the Bokeh visualization on Heroku will take the place of the `publish` stage in the pipeline from HW3.

A Heroku Python application needs, at a minimum, three files to run. All other Heroku-specific files are optional:
- [`Procfile`](https://devcenter.heroku.com/articles/procfile)
- [`requirements.txt`](https://devcenter.heroku.com/articles/python-pip)
- the Python file to run (e.g., your bokeh application Python script).

The Heroku `Procfile` at the base of the application/repository should contain something like the following to launch a bokeh application:
```
web: bokeh serve --port=$PORT --allow-websocket-origin=<app name>.herokuapp.com --address=0.0.0.0 --use-xheaders <bokeh app.py>
```

The `requirements.txt` file placed in the base of the application/repository contains the necessary Python libraries to run your application. It should look something like this:
```
# probably needs numpy
numpy
# need bokeh
bokeh
# might need h5py, if visualization is using it
h5py
# add other non-standard libraries as needed
[...]
```
