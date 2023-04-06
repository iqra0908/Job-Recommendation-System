# Project 3 and Project 4: Job-Recommendation-System 

## Job Matching

This code provides a class called `JobMatching` that matches a given resume to job postings based on keyword and cosine similarity matching. The code uses the `pandas` and `numpy` libraries for data handling, and `CountVectorizer`, `TfidfVectorizer`, and `cosine_similarity` from `sklearn` for text vectorization and similarity matching.

### Requirements

To run this code, you will need to have the following installed:

- Python 3.x
- pandas
- numpy
- scikit-learn (sklearn)

### Deployment
The code is deployed on AWS Athena to train and evaluate the model that pulls data from S3.

### Usage

1. Save the `job_matching.py` file in your desired directory.
2. Create a new Python file in the same directory, and import the `JobMatching` class from `job_matching.py`:
3. Create an instance of the `JobMatching` class:
4. Load the resume and job postings:
5. Use the `get_jobs_matched` method to get a list of job postings that match the given resume:
6. The `matched_jobs` list contains a dictionary for each matched job posting, with the following fields:

- `date`: the date the job posting was posted
- `Title`: the job title
- `Company`: the company name
- `Eligibility`: the eligibility criteria for the job
- `Location`: the job location
- `JobDescription`: the job description
- `JobRequirment`: the job requirements
- `RequiredQual`: the required qualifications for the job
- `ApplicationP`: the application procedure for the job
