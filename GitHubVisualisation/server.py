import requests
import json
from flask import Flask, render_template, request

server = Flask(__name__)
PORT = 8080

@server.route("/")
def index():
    return render_template('index.html')

@server.route("/github", methods =['POST'])
def getGit():
	username = request.form.get('username')
	password = request.form.get('password')

	userRepo = requests.get ("https://api.github.com/users/"+username+"/repos", auth = (username, password))
	allRepo = requests.get ("https://api.github.com/user/repos", auth = (username, password))
	data = userRepo.json()
	allData = allRepo.json()
	commits = []
	for item in allData:
		contributors = []
		repoContributors = requests.get(item['url']+"/contributors", auth=(username, password))
		for contributor in repoContributors.json():
			contributors.append({ 'key': contributor['login'], 'value': contributor['contributions'] })
		commits.append({ 'name': item['name'], 'contributors': contributors })
		"""
		for r in contributorInfo:
			print("Commits for " + r['login']+" = ", r['contributions
		"""
	return render_template('stats.html', json_commits = json.dumps(commits), commits=commits)

if __name__ == "__main__":
    server.run(port=PORT)
