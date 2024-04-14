import os

from git import Repo


class Cloner:
    def __init__(self, output_folder):
        self.output_folder = output_folder

    def create_repository_url(self, repository):
        print("trying to clone " + repository)
        repo_url = "https://github.com/" + repository + ".git"
        print(repo_url)
        return repo_url

    def clone_repository(self, repository):
        repo_url = self.create_repository_url(repository)

        try:
            repo_name = repo_url.split("/")[-1].split(".")[0]
            repo_path = os.path.join(self.output_folder, repo_name)

            if not os.path.exists(repo_path):
                Repo.clone_from(repo_url, str(repo_path))
                print(f"Repository '{repo_name}' cloned successfully.")
                print("ho appena clonato " + str(repo_path))
                return repo_path

        except Exception as e:

            print(f"Failed to clone repository '{repo_url}': {str(e)}")
