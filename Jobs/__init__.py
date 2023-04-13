import sys
sys.path.append('.')
import azure.functions as func
from flask import Flask, request, render_template
from job_matching import JobMatching
from azure.functions import WsgiMiddleware

job = JobMatching()
app = Flask(__name__)

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

# Wrap the Flask app with the WsgiMiddleware
app = WsgiMiddleware(app)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    environ = dict(req.environ)
    response = app(environ)
    return func.HttpResponse(
        body=response[0],
        status_code=response[1],
        headers=response[2]
    )
