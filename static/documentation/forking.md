# Working with a forked repo

## Teminology

**fork** = a fork (copy) of the original repo

**upstream** = the original repo

## Forking the repo

In order to contribute to this project, you will need to create a fork of the repo on your own account.
To fork the repo, just open the repository in a browser and click on the "fork" button on the top right of the page.

![Forking a repo](https://github.com/Code-Institute-Community/ci-hackathon-app/blob/master/static/img/documentation/fork.PNG?raw=true)

If you are part of any organisations, it will ask you which organisation you want to create the fork in.
If you are not part of any, it will automatically create it under your personal GitHub account.

## Cloning the forked code

### Gitpod

1. Open your forked repo in the browser
2. Click on the Gitpod button to open a new workspace

### Local Development

1. Open your forked repo in the browser
2. Click on the "Code" button and copy the link to the repo
3. Open a Terminal window and clone the repo

```
git clone [link to forked repo]
cd ci-hackathon-app
```
4. Add the upstream to the remote

```
# via HTTPS
git remote add upstream https://github.com/Code-Institute-Community/ci-hackathon-app.git

# via SSH
git remote add upstream git@github.com:Code-Institute-Community/ci-hackathon-app.git
``` 

## Creating a Pull Request from a forked repo to the original repo

1. Checkout to a new branch

```
git checkout -b [my-development-branch]
```

2. Make your changes
3. Add and commit your changes to your branch

```
git add .  # all changes or specify file names
git commit -m "Add a commit message here"
```

4. Push your changes to your fork

```
git push origin [my-development-branch]
```

5. Go back to your forked repo in the browser
6. Click on the message saying "Compare & pull request"

![Compare & pull request message](https://github.com/Code-Institute-Community/ci-hackathon-app/blob/master/static/img/documentation/compare-and-pull.png?raw=true)

7. Make sure that the Pull Request is created from the fork to the upstream master branch

![Pull Request](https://github.com/Code-Institute-Community/ci-hackathon-app/blob/master/static/img/documentation/pull-request.png?raw=true)

8. Add details to the Pull Requests

## Update fork with newest changes from upstream

1. Checkout to master (on your fork)

```
git checkout master
```
2. Pull updates from upstream
```
git pull upstream master
```
3. Push changes to fork
```
git push
```
