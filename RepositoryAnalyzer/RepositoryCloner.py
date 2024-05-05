import logging
import os

from git import Repo
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)


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
        repo_path = ""

        try:
            # repo_name = repo_url.split("/")[-1].split(".")[0]
            repo_name = repository.replace("/", "\\")
            repo_path = os.path.join(self.output_folder, repo_name)

            if not os.path.exists(repo_path):
                Repo.clone_from(repo_url, str(repo_path), depth=1)
                logging.info('repository clonata')
                print(f"Repository '{repo_name}' cloned successfully.")
                print("ho appena clonato " + str(repo_path))
                logging.info("ho appena clonato " + str(repo_path))
                return repo_path
            else:
                logging.warning("ho già trovato clonato " + str(repo_path))
                print("ho già trovato clonato " + str(repo_path))
                return repo_path

        except Exception as e:

            logging.warning(f"Problema durante la clonazione della repository '{repo_url}': {str(e)}")
            print(f"Failed to clone repository '{repo_url}': {str(e)}")
            return repo_path

