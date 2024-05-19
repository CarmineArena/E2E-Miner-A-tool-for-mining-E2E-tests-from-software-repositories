from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
import sys

print(sys.path)

sys.path.append("Dataset")
from Dataset.DataSet import DataSet
from Dataset.FilterStrategy import Filter
from RepositoryAnalyzer.Analyzer import AnalyzerController

from Dataset.Repository import Repository

dataset = DataSet()
# tutte = dataset.read_all_repositories()
# Base.metadata.create_all(bind=engine)


# dataset = DataSet('Dataset/results.json')

# tutte = dataset.read_all_repositories()

# for rep in tutte:
# session.add(RepositoryDAO(rep))

filtro = Filter(is_fork=False, commits=2000, contributors=10, stargazers=100, languages=['Java', 'Python', 'JavaScript', 'TypeScript'])
risultati_filtrati = dataset.filter_repositories(filtro)

# filtroJava = Filter(is_fork=False, commits=2000, contributors=10, stargazers=100, languages=['Java'])
# risultati_Java = dataset.filter_repositories(filtroJava)
# filtroPython = Filter(is_fork=False, commits=2000, contributors=10, stargazers=100, main_language=['Python'])
# risultati_Python = dataset.filter_repositories(filtroPython)

# filtroJS = Filter(is_fork=False, commits=2000, contributors=10, stargazers=100, main_language=['JavaScript'])
# risultati_JS = dataset.filter_repositories(filtroJS)

# print(len(tutte))
# print("di cui " + str(len(risultati_filtrati)) + " sono repositories fatte con Java, Python, o JavaScript")
# print("di cui " + str(len(risultati_Java)) + " sono scritti in Java, " + str(len(risultati_Python)) + " sono scritti in Python e " + str(len(risultati_JS)) + " sono scritti in JavaScript")
# print(str(len(risultati_Java)) + "con Java")
# print(risultati_Java)

# print(risultati_JS)

analyzer = AnalyzerController(risultati_filtrati)
analyzer.analyze_repositories()
