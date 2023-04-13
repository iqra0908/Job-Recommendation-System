import sys
sys.path.append('.')
import azure.functions as func
from flask import Flask, request, render_template
from job_matching import JobMatching

app = Flask(__name__)
job = JobMatching()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/jobs', methods=['GET'])
def getJobs():
    return job.get_all_jobs()

@app.route('/jobsByResume', methods=['POST'])
def getJobsMatchedWithResume():
    if 'resume' in request.data.decode():
        resume = request.data.decode()
    else:
        # If no resume data is found, return an error message
        return "Error: No resume data provided."

    # Pass the resume data to the get_jobs_matched() function
    return job.get_jobs_matched(resume)

def main(req: func.HttpRequest) -> func.HttpResponse:
    with app.app_context():
        response = app.make_response(index())
        headers = {}
        for key, value in response.headers.items():
            headers[key] = value
        return func.HttpResponse(
            body=response.get_data(),
            status_code=response.status_code,
            headers=headers
        )