mod job_matching;

fn main() {
    let mut job_matching = job_matching::JobMatching::new();
    let resume = job_matching.load_resume();
    let results = job_matching.get_jobs_matched(&resume);
    println!("{:?}", results);
}
