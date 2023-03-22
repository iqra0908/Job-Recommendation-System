use job_matching::JobMatching;
use rocket::http::Status;
use rocket::response::status;
use rocket::{get, post, routes, Rocket};
use serde::{Deserialize, Serialize};
use std::io;
use std::path::{Path, PathBuf};

#[derive(Debug, Deserialize, Serialize)]
struct Resume {
    resume: String,
}

#[get("/")]
fn index() -> io::Result<rocket_contrib::templates::Template> {
    let context = serde_json::json!({});
    rocket_contrib::templates::Template::render("index", &context)
}

#[get("/jobs")]
fn get_jobs() -> status::Custom<String> {
    let job = JobMatching::new();
    let jobs = job.get_all_jobs();
    status::Custom(Status::Ok, jobs)
}

#[post("/jobsByResume", format = "json", data = "<resume>")]
fn get_jobs_matched_with_resume(resume: serde_json::Result<Resume>) -> status::Custom<String> {
    match resume {
        Ok(resume) => {
            let job = JobMatching::new();
            let jobs = job.get_jobs_matched(resume.resume);
            status::Custom(Status::Ok, jobs)
        }
        Err(err) => {
            status::Custom(Status::BadRequest, format!("Error: {}", err))
        }
    }
}

fn rocket() -> Rocket {
    rocket::ignite()
        .mount("/", routes![index, get_jobs, get_jobs_matched_with_resume])
        .attach(rocket_contrib::templates::Template::fairing())
}

fn main() {
    rocket().launch();
}
