import ConfigParser

def parse_conf(project_job):
    full_conf = {}
    try:
        conf = ConfigParser.ConfigParser()
        file_output = conf.read(project_job)

        project_name_list = conf.sections()

        for project_name in project_name_list:
            file_output = read_conf(project_name, project_job)

            full_conf[project_name]=file_output
        return full_conf

    except:
        print ('could not parse the file.')


def read_conf(project_job, file):
    config_info = {}
    try:
        conf = ConfigParser.ConfigParser()
        conf.read(file)

        project_name = project_job

        config_info['port'] = conf.get(project_name, 'port')
        config_info['jobs'] = conf.get(project_name, 'jobs').split(',')
        config_info['ip'] = conf.get(project_name, 'ip')
        config_info['username'] = conf.get(project_name, 'username')
        config_info['password'] = conf.get(project_name, 'password')
        config_info['history'] = conf.get(project_name, 'history')
        return config_info

    except:
        print ('could not read value of sections')

