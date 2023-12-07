import os

def generate_template(words, template_path, target_project_folder):
    if not os.path.exists(target_project_folder):
        os.makedirs(target_project_folder)
    # get list of file from path
    files = os.listdir(template_path)
    print(files)

    for template_file in files:
        template_path_file = template_path + "/" + template_file
        project_path_file = target_project_folder + "/" + template_file
        print('template_path_file', template_path_file)

        # get file and replace in the template each words from array by names and values {domain: value, organization: value}
        with open(template_path_file, 'r') as file:
            template = file.read()

        # list in for loop value and name from array elements
        for key, value in words.items():
            template = template.replace("{" + key + "}", value)

        print(f"Template {template_path_file}: {template}")
        # save the template in path
        with open(project_path_file, 'w') as file:
            file.write(template)