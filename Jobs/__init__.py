import logging
import sys
sys.path.append('.')
import azure.functions as func
from scripts.job_matching import JobMatching
from flask import Flask, request, render_template
import azure.functions as func

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

if __name__ == "__main__":
    app.run()
