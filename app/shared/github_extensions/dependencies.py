from github.Organization import Organization
from github.Team import Team
from github.Repository import Repository
from pprint import pp
from string import Template
import requests
from shared.logger.out import Out


class Dependencies:
    """ Extra class to handle dependency data """
    endpoint:str = 'https://api.github.com/graphql'


    def build_query(self, owner:str, repository:str):
        """
        Use string tempplating to generate a graphql friendly template with
        variables substituted
        """
        Out.debug(f"[{repository}] Generating template for graphgl query")
        template = Template(
        """{
            repository(owner:"$owner", name:"$name") {
                dependencyGraphManifests {
                    totalCount
                    nodes {
                        filename
                    }
                    edges {
                        node {
                            blobPath
                            dependencies {
                                totalCount
                                nodes {
                                    packageName
                                    requirements
                                    hasDependencies
                                    packageManager
                                }
                            }
                        }
                    }
                }
            }
        }"""
        )
        query = template.substitute(owner=owner, name=repository)
        return query

    def run(self, query, headers):
        """
        Call the graphql API endpoint
        """
        Out.debug(f"Calling api [{self.endpoint}]")
        request = requests.post(self.endpoint, json={'query': query}, headers=headers)
        if request.status_code != 200:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        return dict( request.json() ).get('data', None).get('repository', None).get('dependencyGraphManifests')


    def format(self, from_api:dict, owner:str, repository:Repository) -> tuple:
        """
        Convert the API returned data into source list and package list we've used historically
        """
        packages = []
        sources = []
        branch = repository.default_branch
        link = f"<a href='{repository.html_url}'>{repository.full_name}</a>"
        # get all the files
        for f in from_api.get('nodes', []):
            sources.append(f.get('filename', None))

        # get all packages mapped in new format
        for edge in from_api.get('edges', []):
            node = edge.get('node', {})
            source = node.get('blobPath', None).replace(f"/{owner}/{repository.name}/blob/{branch}", ".")
            deps = node.get('dependencies', {})
            for dep in deps.get('nodes', []):
                Out.debug(f"[{owner}/{repository}] Package [{dep.get('packageName')}] with versions [{dep.get('requirements')}] in [{source}]")
                p = {
                    'Repository': link,
                    'Package': dep.get('packageName', None),
                    'Versions': dep.get('requirements', None),
                    'Source': source,
                    'PackageManager': dep.get('packageManager', None)
                }
                packages.append(p)
        return packages, sources


    def get(self,
        org:str,
        team:Team,
        repository:Repository,
        token:str,
        preview_header:str = "application/vnd.github.hawkgirl-preview+json") -> tuple:
        """
        Fetch dependency data
        """
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": preview_header
        }
        Out.debug(f"[{repository.full_name}/{team.name}] Calling preview api [{preview_header}]")
        query = self.build_query(org, repository.name)
        from_api = self.run(query, headers)
        return self.format(from_api, org, repository)
