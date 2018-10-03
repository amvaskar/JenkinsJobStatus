import urllib2, base64
import json
import conf_reader

def parsing_project_prop(parse_conf):
	file_name = 'project_job.conf'
	project_prop = conf_reader.parse_conf(file_name)

	final_project_dict = {}
	for project in project_prop:

		username = parse_conf[project]['username']
		jobs = parse_conf[project]['jobs']
		ip = parse_conf[project]['ip']
		password = parse_conf[project]['password']
		port = parse_conf[project]['port']
		history = parse_conf[project]['history']

		job_values = job(jobs, port, ip, history, username, password)

		final_project_dict[project] = job_values
	return final_project_dict

def job(jobname, port, ip, history_number, username, password):

	history_number =int(history_number)
	final_dictionary = {}

	for job in jobname:
		list_job_success = []
		list_job_failure = []
		list_job_abort = []
		list_job_others = []
		result_list = []

		try:
			user_name= username
			passwd= password
			job_name= job.strip()
			request = urllib2.Request("http://%s:%s/job/%s/lastBuild/api/json?pretty=true" % (ip,port,job_name))

			base64string = base64.encodestring('%s:%s' % (user_name, passwd)).replace('\n', '')
			request.add_header("Authorization", "Basic %s" % base64string)

			result = urllib2.urlopen(request)
			json_result = result.read()
			lastBuild_number = json.loads(json_result)['number']
			lastBuild_number +=1

		except:
			print ("\nCheck jenkins build status \n")

		try:
			if history_number >= lastBuild_number or history_number == 0:

				for i in range(1, lastBuild_number):

					firstpart = "http://%s:%s/job/" %(ip, port)
					job_number = str(i)
					secondpart = "/api/json?pretty=true"
					final_url = (firstpart + '%s' + "/" + job_number + secondpart) %(job_name)
					request = urllib2.Request(final_url)
					base64string = base64.encodestring('%s:%s' % (user_name, passwd)).replace('\n', '')
					request.add_header("Authorization", "Basic %s" % base64string)
					result = urllib2.urlopen(request)
					json_result_2 = result.read()

					jobStatus = json.loads(json_result_2)
					result_value = jobStatus['result']

					if result_value == 'SUCCESS':
						list_job_success.append(result_value)

					elif result_value == 'FAILURE':
						list_job_failure.append(result_value)

					elif result_value == 'ABORTED':
						list_job_abort.append(result_value)

					elif result_value != 'SUCCESS' and result_value != 'FAILURE' and result_value != 'ABORTED':
						list_job_others.append(result_value)

					else:
						print ("Error on json file from jenkins!!")

				history_number = lastBuild_number -1

			else:
				for i in range(lastBuild_number - history_number, lastBuild_number):

					firstpart = "http://%s:%s/job/" %(ip, port)
					job_number = str(i)
					secondpart = "/api/json?pretty=true"
					final_url = (firstpart + '%s' + "/" + job_number + secondpart) %(job_name)
					request = urllib2.Request(final_url)
					base64string = base64.encodestring('%s:%s' % (user_name, passwd)).replace('\n', '')
					request.add_header("Authorization", "Basic %s" % base64string)
					result = urllib2.urlopen(request)
					json_result_2 = result.read()

					jobStatus = json.loads(json_result_2)
					result_value = jobStatus['result']

					if result_value == 'SUCCESS':
						list_job_success.append(result_value)

					elif result_value == 'FAILURE':
						list_job_failure.append(result_value)

					elif result_value == 'ABORTED':
						list_job_abort.append(result_value)

					elif result_value != 'SUCCESS' and result_value != 'FAILURE' and result_value != 'ABORTED':
						list_job_others.append(result_value)

					else:
						print ("Error on json file from jenkins!!")

			result_list.append(len(list_job_success))
			result_list.append(len(list_job_failure))
			result_list.append(len(list_job_abort))
			result_list.append(len(list_job_others))
			result_list.append(history_number)

		except:
			print('Error on project credentials !!')

		final_dictionary[job_name] = result_list


	return final_dictionary

