import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobMatching:
    def __init__(self):
        self.jobs = self.load_jobs()#.head(500)

    
    def load_resume(self):
        resume = open("data/Resume-Iqra-2023.txt").read()
        return resume
    
    def load_jobs(self):
        jobs = pd.read_csv("data/dataworld-jobs.csv")
        jobs.dropna(subset=['Job Description'], inplace=True)
        jobs.fillna('', inplace=True)
        jobs = jobs.rename(columns={'Job Title': 'JobTitle', 'Job Description': 'JobDescription', 'Job Type':'JobType'})
        return jobs
    
    def get_all_jobs(self):
        jobs = self.jobs
        jobs = jobs[['JobTitle', 'JobDescription', 'JobType', 'Categories',
       'Location', 'City', 'State', 'Country', 'Zip Code', 'Address',
       'Salary From', 'Salary To', 'Salary Period', 'Apply Url', 'Apply Email',
       'Employees', 'Industry', 'Company Name', 'Employer Email',
       'Employer Website', 'Employer Phone', 'Employer Logo',
       'Companydescription', 'Employer Location', 'Uniq Id',
       'Crawl Timestamp']]
        return jobs.head(20).to_dict(orient='records')
    
    def keyword_matching(self,resume,jobs):
        vectorizer = CountVectorizer()
        keywords = vectorizer.fit_transform([resume]).toarray()[0]

        keywords_match = []
        for i in range(len(jobs)):
            job_description_keywords = vectorizer.transform([jobs['JobDescription'].iloc[i]]).toarray()[0]
            job_requirement_keywords = vectorizer.transform([jobs['JobRequirment'].iloc[i]]).toarray()[0]
            match = all(job_description_keywords[i] >= keywords[i] or job_requirement_keywords[i] >= keywords[i] for i in range(len(keywords)))
            keywords_match.append(match)

        # Add keywords_match column to books dataframe
        jobs['keywords_match'] = keywords_match
        
    def cosine_similarity(self,resume,jobs):
        vectorizer = TfidfVectorizer()
        resume_vector = vectorizer.fit_transform([resume])

        similarity_scores = []
        for i in range(len(jobs)):
            job_vector = vectorizer.transform([jobs['JobDescription'].iloc[i]])
            similarity = cosine_similarity(resume_vector, job_vector)[0][0]
            similarity_scores.append(similarity)
            
        jobs['cosine_similarity'] = similarity_scores
        
    def get_jobs_matched(self,resume):
        jobs = self.jobs
        self.cosine_similarity(resume,jobs)
        jobs = jobs.sort_values(by=['cosine_similarity'], ascending=False)
        #jobs = jobs[['date','Title','Company','Eligibility','Location','JobDescription','JobRequirment','RequiredQual','ApplicationP']]
        return jobs.head(20).to_dict(orient='records')
        
if __name__ == '__main__':
    job_matching = JobMatching()
    resume = job_matching.load_resume()
    results = job_matching.get_jobs_matched(resume)
    print(results)
    

        