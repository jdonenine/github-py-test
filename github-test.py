import uuid
from github import Github

# This is a small script that does the following to quickly test how tokens work within GitHub:
# * Connect/Login to GitHub using a provided personal-access-token (gh_token)
# * Fork an exsiting repo (gh_repo)
# * Create a branch in the forked repo
# * Create a new file on the new branch in the forked repo
# * Generate a PR in the original repo (gh_repo) to merged from the forked repo back into the original

gh_repo = ''
gh_token = ''

# Connect to GitHub and gather info about the user
# provided by the token

gh = Github(gh_token)

# Retrieve the user provided by the token
user = gh.get_user()
# Spit out information about the user
print('Using GitHub token: %s' % gh_token)
print('GitHub user id: %s' % user.id)
print('GitHub user login: %s' % user.login)
print('GitHub user name: %s' % user.name)
print('GitHub user email: %s' % user.email)
print('GitHub user company: %s' % user.company)

# Retrieve the repo that we will try to create
# a branch within
print('Accessing repository: %s' % gh_repo)
repo = gh.get_repo(gh_repo)

# Retrieve the branch we want to target
default_branch_name = repo.default_branch

# Fork the repo
print('Forking repository: %s' % repo.full_name)
fork = repo.create_fork()
print('Forked repository: %s' % fork.full_name)

# Access the branch on the forked repo
print('Accessing default branch: %s' % default_branch_name)
source_branch = fork.get_branch(default_branch_name)

# Create a new branch
uuid_str = str(uuid.uuid4())
new_branch_name = "_".join([user.login, uuid_str])
print('Creating branch: %s' % new_branch_name)
new_branch_ref = fork.create_git_ref(ref = "refs/heads/" + new_branch_name, sha = source_branch.commit.sha)

# Get the new branch
print('Accessing branch: %s' % new_branch_name)
new_branch = fork.get_branch(new_branch_name)

# Simulate a change on the branch
file_path = 'test-' + uuid_str + '.txt'
file_content = 'Testing, Testing, Testing ' + uuid_str
fork.create_file(path = file_path, message = "Test Content " + uuid_str, content = file_content, branch = new_branch_name)

# create a PR from the fork branch into the original branch
pr_name = pr_body = "Test changes for uuid " + uuid_str
print('Creating PR: %s' % pr_name)
pr = repo.create_pull(title = pr_name, body = pr_body, base = default_branch_name, head = user.login + ':' + new_branch_name)
print('Created PR at: %s' % pr.html_url)
