# Project 3 and Project 4: Job-Recommendation-System 

## Job Matching

This code provides a class called `JobMatching` that matches a given resume to job postings based on keyword and cosine similarity matching. The code uses the `pandas` and `numpy` libraries for data handling, and `CountVectorizer`, `TfidfVectorizer`, and `cosine_similarity` from `sklearn` for text vectorization and similarity matching.

This is a job matching system that matches job seekers with suitable job openings based on their resumes. The system uses the cosine similarity metric to determine the similarity between the keywords in the job seeker's resume and the job description of each job opening.

## Requirements

- pandas
- numpy
- scikit-learn
- gensim
- tensorflow
- keras

## Installation

You can install the required packages by running the following command:
`pip install -r requirements.txt`

### Deployment for Project 3
The code is deployed on AWS Athena to train and evaluate the model that pulls data from S3.

### Deployment for Project 4
The code is deployed on Azure functions app as a function for flask app.

### Dataset
https://data.world/promptcloud/indeed-job-posting-dataset

### Usage


## Usage

To use the job matching system, follow these steps:

1. Prepare the job data: The job data should be in a CSV format with the following columns: JobTitle, JobDescription, JobType, Categories, Location, City, State, Country, Zip Code, Address, Salary From, Salary To, Salary Period, Apply Url, Apply Email, Employees, Industry, Company Name, Employer Email, Employer Website, Employer Phone, Employer Logo, Companydescription, Employer Location, Uniq Id, Crawl Timestamp.

2. Load the job data: In the `JobMatching` class, use the `load_jobs()` method to load the job data into a pandas DataFrame.

3. Load the resume: In the `JobMatching` class, use the `load_resume()` method to load the resume data from a text file.

4. Match the resume with the jobs: In the `JobMatching` class, use the `get_jobs_matched(resume)` method to match the resume with the jobs. This method returns a list of the top 20 jobs that match the resume.

## Contributing

Contributions are welcome! If you have any suggestions or find any bugs, please feel free to open an issue or submit a pull request.
