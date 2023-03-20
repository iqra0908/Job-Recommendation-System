import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#sys.path.append('../')

class JobMatching:
    def __init__(self):
        self.jobs = self.load_jobs().head(500)
    
    def load_resume(self):
        resume = open("data/Resume-Iqra-2023.txt").read()
        return resume
    
    def load_jobs(self):
        jobs = pd.read_csv("data/job_posts.csv")
        jobs.dropna(subset=['JobDescription','JobRequirment'], inplace=True)
        jobs.fillna('', inplace=True)
        return jobs
    
    def get_all_jobs(self):
        jobs = self.jobs
        jobs = jobs[['date','Title','Company','Eligibility','Location','JobDescription','JobRequirment','RequiredQual','ApplicationP']]
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
        #req_similarity_scores = []
        for i in range(len(jobs)):
            job_vector = vectorizer.transform([jobs['jobpost'].iloc[i]])
            #job_requirement_vector = vectorizer.transform([jobs['JobRequirment'].iloc[i]])
            similarity = cosine_similarity(resume_vector, job_vector)[0][0]
            #req_similarity = cosine_similarity(resume_vector, job_requirement_vector)[0][0]
            similarity_scores.append(similarity)
            #req_similarity_scores.append(req_similarity)
            
        jobs['cosine_similarity'] = similarity_scores
        
    def get_jobs_matched(self,resume):
        jobs = self.jobs
        self.cosine_similarity(resume,jobs)
        jobs = jobs.sort_values(by=['cosine_similarity'], ascending=False)
        jobs = jobs[['date','Title','Company','Eligibility','Location','JobDescription','JobRequirment','RequiredQual','ApplicationP']]
        return jobs.head(20).to_dict(orient='records')
        
if __name__ == '__main__':
    job_matching = JobMatching()
    resume = job_matching.load_resume()
    jobs = job_matching.load_jobs()
    #job_matching.keyword_matching(resume,jobs)
    job_matching.cosine_similarity(resume,jobs)
    print(jobs[jobs['desc_similarity'] > 0.5])
    #print(jobs[jobs['keywords_match']])
    

        