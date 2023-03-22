use std::fs::File;
use std::io::Read;
use std::collections::HashMap;
use std::vec::Vec;

use csv::ReaderBuilder;
use ndarray::{Array1, Array2};
use ndarray_linalg::norm::Norm;
use ndarray_stats::QuantileExt;
use serde::{Deserialize, Serialize};
use nlp_units::{tfidf_vectorize, cosine_similarity};

#[derive(Debug, Deserialize, Serialize)]
struct JobPosting {
    date: String,
    Title: String,
    Company: String,
    Eligibility: String,
    Location: String,
    JobDescription: String,
    JobRequirment: String,
    RequiredQual: String,
    ApplicationP: String,
}

struct JobMatching {
    jobs: Vec<JobPosting>,
}

impl JobMatching {
    fn new() -> JobMatching {
        let jobs = JobMatching::load_jobs().unwrap();
        JobMatching {
            jobs: jobs.iter().take(500).cloned().collect(),
        }
    }

    fn load_resume(&self) -> String {
        let mut file = File::open("data/Resume-Iqra-2023.txt").unwrap();
        let mut contents = String::new();
        file.read_to_string(&mut contents).unwrap();
        contents
    }

    fn load_jobs() -> Result<Vec<JobPosting>, csv::Error> {
        let file = File::open("data/job_posts.csv").unwrap();
        let mut reader = ReaderBuilder::new()
            .has_headers(true)
            .delimiter(b',')
            .flexible(true)
            .from_reader(file);

        let mut jobs = Vec::new();

        for result in reader.deserialize() {
            let record: JobPosting = result?;
            if !record.JobDescription.is_empty() && !record.JobRequirment.is_empty() {
                jobs.push(record);
            }
        }

        Ok(jobs)
    }

    fn get_all_jobs(&self) -> Vec<HashMap<String, String>> {
        let mut jobs = Vec::new();

        for job in &self.jobs {
            let mut job_map = HashMap::new();
            job_map.insert("date".to_string(), job.date.clone());
            job_map.insert("Title".to_string(), job.Title.clone());
            job_map.insert("Company".to_string(), job.Company.clone());
            job_map.insert("Eligibility".to_string(), job.Eligibility.clone());
            job_map.insert("Location".to_string(), job.Location.clone());
            job_map.insert("JobDescription".to_string(), job.JobDescription.clone());
            job_map.insert("JobRequirment".to_string(), job.JobRequirment.clone());
            job_map.insert("RequiredQual".to_string(), job.RequiredQual.clone());
            job_map.insert("ApplicationP".to_string(), job.ApplicationP.clone());

            jobs.push(job_map);
        }

        jobs
    }


    fn keyword_matching(resume: &str, jobs: &mut Vec<HashMap<String, String>>) {
        let mut vectorizer = CountVectorizer::new();
        let keywords = vectorizer.fit_transform(vec![resume]).unwrap().toarray().unwrap().remove(0);

        let mut keywords_match = vec![];
        for i in 0..jobs.len() {
            let job_description_keywords = vectorizer.transform(vec![&jobs[i]["JobDescription"]]).unwrap().toarray().unwrap().remove(0);
            let job_requirement_keywords = vectorizer.transform(vec![&jobs[i]["JobRequirment"]]).unwrap().toarray().unwrap().remove(0);
            let mut match_found = true;
            for j in 0..keywords.len() {
                if job_description_keywords[j] < keywords[j] && job_requirement_keywords[j] < keywords[j] {
                    match_found = false;
                    break;
                }
            }
            keywords_match.push(match_found);
        }

        // Add keywords_match column to jobs vector of hashmaps
        for i in 0..jobs.len() {
            jobs[i].insert("keywords_match".to_string(), keywords_match[i].to_string());
        }
    }


    fn cosine_similarity(&mut self, resume: &str, jobs: &mut DataFrame) {
        let vectorizer = TfidfVectorizer::default();
        let resume_vector = vectorizer.fit_transform(&[resume]);

        let mut similarity_scores = Vec::new();
        for i in 0..jobs.height() {
            let job_vector = vectorizer.transform(&[jobs["jobpost"][i].clone()]);
            let similarity = cosine_similarity(&resume_vector, &job_vector)[0][0];
            similarity_scores.push(similarity);
        }

        jobs.add_column("cosine_similarity".to_string(), Series::new(similarity_scores));
    }

    fn get_jobs_matched(&self, resume: &str) -> Vec<HashMap<String, String>> {
        let mut jobs = self.jobs.clone();
        self.cosine_similarity(resume, &mut jobs);
        jobs.sort_by(|a, b| b["cosine_similarity"].partial_cmp(&a["cosine_similarity"]).unwrap());
        jobs = jobs.iter().map(|job| {
            let mut filtered_job = HashMap::new();
            filtered_job.insert("date".to_string(), job["date"].clone());
            filtered_job.insert("Title".to_string(), job["Title"].clone());
            filtered_job.insert("Company".to_string(), job["Company"].clone());
            filtered_job.insert("Eligibility".to_string(), job["Eligibility"].clone());
            filtered_job.insert("Location".to_string(), job["Location"].clone());
            filtered_job.insert("JobDescription".to_string(), job["JobDescription"].clone());
            filtered_job.insert("JobRequirment".to_string(), job["JobRequirment"].clone());
            filtered_job.insert("RequiredQual".to_string(), job["RequiredQual"].clone());
            filtered_job.insert("ApplicationP".to_string(), job["ApplicationP"].clone());
            filtered_job
        }).collect();
        jobs.truncate(20);
        jobs
    }
}

fn main() {
    let mut job_matching = JobMatching::new();
    let resume = job_matching.load_resume();
    let results = job_matching.get_jobs_matched(&resume);
    println!("{:?}", results);
}
    
