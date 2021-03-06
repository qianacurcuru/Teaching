import json
import urllib2
import requests,sys

choice = raw_input('Email upoload or contributor key [1/2] ')

while choice != '1' and choice != '2':
    print "Not a valid input"
    choice = raw_input('Email upoload or contributor key [1/2] ')

if choice == '1': #Email uploader

    project = raw_input('Enter a project id: ')

    project_response_code = requests.get('http://rsense-dev.cs.uml.edu/api/v1/projects/'+project)

    while project_response_code.status_code != 200:
        print "Not a valid project \n"
        project = raw_input('Enter a project id: ')

        project_response_code = requests.get('http://rsense-dev.cs.uml.edu/api/v1/projects/'+project)

    data = json.load(urllib2.urlopen('http://rsense-dev.cs.uml.edu/api/v1/projects/'+project))

    title = raw_input('Enter a dataset title: ')
    email = raw_input('Enter email: ')
    password = raw_input('Enter password: ')
    credential_checker = requests.get('http://rsense-dev.cs.uml.edu/api/v1/users/myInfo?email='+email+'&password='+password)

    while credential_checker.status_code != 200:
        print "Incorrect email or password"
        email = raw_input('Enter email: ')
        password = raw_input('Enter password: ')
        credential_checker = requests.get('http://rsense-dev.cs.uml.edu/api/v1/users/myInfo?email='+email+'&password='+password)

    number = raw_input('Enter a number to be uploaded: ')
    url = 'http://rsense-dev.cs.uml.edu/api/v1/projects/'+project+'/jsonDataUpload'

    payload = {
        'email': email,
        'password': password,
        'title': title,
        'data':
        {
            ''+ str(data['fields'][0]['id']): [number]
        }
    }

    headers = {'content-type': 'application/json'}

    print "\nUPLOADING TO iSENSE."

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    if r.status_code == 200:
        print "\nUploaded fine, with a code of 200!"

elif choice == '2': #Contributor Key Uploading
    project = raw_input('Enter a project id: ')

    project_response_code = requests.get('http://rsense-dev.cs.uml.edu/api/v1/projects/'+project)

    while project_response_code.status_code != 200:
        print "Not a valid project \n"
        project = raw_input('Enter a project id: ')

        project_response_code = requests.get('http://rsense-dev.cs.uml.edu/api/v1/projects/'+project)

    data = json.load(urllib2.urlopen('http://rsense-dev.cs.uml.edu/api/v1/projects/'+project))

    contributor_name = raw_input("Enter a contibutor name: ")
    title = raw_input("Enter the title of the dataset: ")
    number = raw_input("Enter a number: ")
    contributor_key = raw_input("Enter a contributor key: ")

    print "\nUPLOADING TO iSENSE."

    # POST stuff.
    url = 'http://rsense-dev.cs.uml.edu/api/v1/projects/683/jsonDataUpload'
    payload = {
        'title': title,                     # Note, spent forever trying to figure this out.
        'contribution_key': contributor_key,    # But it's contribution_key - not contributor_key
        'contributor_name': contributor_name,   
        'data':
        {
            ''+ str(data['fields'][0]['id']): [number]
        }
    }

    # This is needed, otherwise I got code 422s and the data wasn't showing up right in the log.
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    while r.status_code == 401:
        print "Wrong contributor key"
        contributor_key = raw_input("Enter a contributor key: ")

        print "\nUPLOADING TO iSENSE."

        # POST stuff.
        url = 'http://rsense-dev.cs.uml.edu/api/v1/projects/683/jsonDataUpload'
        payload = {
            'title': title,                     # Note, spent forever trying to figure this out.
            'contribution_key': contributor_key,    # But it's contribution_key - not contributor_key
            'contributor_name': contributor_name,   
            'data':
            {
                ''+ str(data['fields'][0]['id']): [number]
            }
        }

        # This is needed, otherwise I got code 422s and the data wasn't showing up right in the log.
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)

    # Detects status codes and tells the user what went right or wrong.
    if r.status_code == 200:
        print "\nUploaded fine, with a code of 200!"
