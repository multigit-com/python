import sys
sys.path.append('../')
from function.flat_array import flat_array
from function.differenceElementsInArrays import differenceElementsInArrays
from local.fromFilenametoLinesAsArray import fromFilenametoLinesAsArray
from local.generate_template import generate_template
from local.load_file import load_file
from github.get_param_from_repo import get_param_from_repo
from github.create_repo_on_github_and_local import create_repo_on_github_and_local


# check the expected repository list and create if they are not existing on github organisation
# load each line as repository name from '.folders' file, if the repository not existing, create the folder and create the repository on github
# load the description of the repository from '.description.txt' file
# load the default branch from '.default_branch.txt' file
def create_notexisting_folder(api_token, org_name, repos, path_folder, domain, root_path, default_branch = 'main'):
    folders_path = root_path + "/.folders"
    expected_folders = fromFilenametoLinesAsArray(folders_path)
    if not expected_folders:
        exit()
    #print(repos)
    repos_in_orgs = flat_array(repos, 'name')
    print(repos_in_orgs)
    # Call the function with your arrays
    # result = arrayElementsAreIncluded(expected_folders, repos_in_orgs)
    # print(result)
    not_existing_folder = differenceElementsInArrays(expected_folders, repos_in_orgs)
    print(not_existing_folder)


    if not_existing_folder:
        for repo_folder in not_existing_folder:
            branch = get_param_from_repo(repos, 'default_branch')
            if not branch:
                branch = default_branch
            words = {
                'domain': domain,
                'homepage': "http://" + repo_folder + "." + domain,
                'repository': repo_folder,
                'organization': org_name,
                'branch': branch
            }
            template_path = root_path + "/templates/" + repo_folder
            print(template_path)
            target_path=path_folder + "/" + repo_folder
            generate_template(words, template_path, target_path)
            description = load_file(target_path + "/description.txt")
            # create repository on github by api call
            create_repo_on_github_and_local(api_token, org_name, repo_folder, target_path, description, domain)