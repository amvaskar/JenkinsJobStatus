
from flask import Flask, render_template
import jenkins_jobstatus
import conf_reader

file_name= 'project_job.conf'
file_output = conf_reader.parse_conf(file_name)

app = Flask(__name__)\

@app.route("/jenkinsjobstatus")
def jobstatus():

    status = jenkins_jobstatus.parsing_project_prop(file_output)
    return render_template("table.html", status=status)

if __name__ == "__main__":
    app.run(debug=True, port=5005)

