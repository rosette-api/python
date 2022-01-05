## Developer Information

#### Sonar Scanning
* Uncomment the `sonar.branch.name` line in `sonar-project.properties` and adjust the value to match your branch name.
* Install the `coverage` module in to your virtual environment.
  ```
  virtualenv -p python3 ~/venvs/python-binding-development
  source ~/venvs/python-binding-development/bin/activate
  pip install --upgrade pip
  pip install coverage
  ```
* Generate the coverage data.
  ```
  coverage run --source=rosette -m pytest
  ```
* Check the results locally
  ```
  coverage report
  ```
* Generate the XML coverage report
  ```
  coverage xml
  ```
* Push the results to Sonar
  ```
  docker run \
      --rm \
      -e SONAR_HOST_URL="${sonar_host}" \
      -e SONAR_LOGIN="${sonar_token}" \
      -v "$(pwd):/usr/src" \
      sonarsource/sonar-scanner-cli

  ```

### Testing
To test changes you have made to the binding, you can use a pre-configured Docker environment.  This environment will:
- Compile the binding within the container.
- Install the binding within the container.
- Execute one or more example files using the installed binding.
- The example files can be executed against a Cloud release or an Enterprise release.
- If a test suite exists, it will also be executed.

```
git clone git@github.com:rosette-api/python.git
cd python
# Modify the binding...
docker run -e API_KEY=$API_KEY -v $(pwd):/source rosetteapi/docker-python
```

Optional parameters for the `docker run` execution are:

- `-e ALT_URL=<alternative URL>`
  - For testing against an Enterprise environment or the staging environment.
- `-e FILENAME=<single filename>`
  - For testing a single example file instead of all the example files.

To alter the behavior of the pre-configured Docker environment, you can see the Dockerfile source and entry-point
script [here](https://git.basistech.net/raas/rapid-development-tools/tree/master/binding-dockerfiles). 

### Documentation Generation
The existing README for documentation generation is [here](docs/README.md).
The next time the API documentation is touched, please refresh the README and migrate it here.

### Examples README
There's an old [Docker README](examples/docker) in the examples directory that might be a candidate for removal.

### Building A Release
See the [instructions](https://git.basistech.net/raas/rapid-development-tools/tree/master/publish)

### TODOs
- Inconsistent references with `rosette_api` and `rosette-api`
- Doc generation README cleanup?
- Example Docker file still needed?
- `docker-compose.yaml` still needed?
