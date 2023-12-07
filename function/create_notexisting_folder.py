import sys
sys.path.append('../')
from function.fromFilenametoLinesAsArray import fromFilenametoLinesAsArray
from function.flat_array import flat_array
from function.differenceElementsInArrays import differenceElementsInArrays
from function.generate_template import generate_template
from function.load_file import load_file
from function.create_repo_on_github import create_repo_on_github
from function.get_param_from_repo import get_param_from_repo
import os



def create_notexisting_folder(api_token, org_name, repos, path_folder, domain):
    folders_path = os.path.dirname(os.path.realpath(__file__)) + "/.folders"
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
            words = {
                'domain': domain,
                'homepage': "http://" + repo_folder + "." + domain,
                'repository': repo_folder,
                'organization': org_name,
                'branch': get_param_from_repo(repos, 'default_branch')
            }
            template_path = os.path.dirname(os.path.realpath(__file__)) + "/templates/" + repo_folder
            print(template_path)
            target_path=path_folder + "/" + repo_folder
            generate_template(words, template_path, target_path)
            description = load_file(target_path + "/description.txt")
            # create repository on github by api call
            create_repo_on_github(api_token, org_name, repo_folder, target_path, description, domain)