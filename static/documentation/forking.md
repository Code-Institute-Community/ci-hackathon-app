# Working with a forked repo

## Teminology

**fork** = a fork (copy) of the original repo

**upstream** = the original repo

## Forking the repo

In order to contribute to this project you will need to create a fork of the repo on your own account. 
To fork the repo just open the repository in a browser and click on the "fork" button on the top right of the page.

![Forking a repo](https://github.com/Code-Institute-Community/ci-hackathon-app/blob/forking-md/static/img/documentation/fork.PNG?raw=true)

If you are part of any organisations it will ask you which organisation you want to create the fork in.
If you are not part of any, it will automatically create it under your personal GitHub account.

## Cloning the forked code

### Gitpod

1. Open your forked repo in the browser
2. Click on the GitPod button to open a new workspace

### Local Development

1. Open your forked repo in the browser
2. Click on the "Code" button and copy the link to the repo
3. Open a Terminal window and clone the repo
```
git clone [link to forked repo]
cd ci-hackathon-app
```

## Creating a Pull Request from a forked repo to the original repo

3. Checkout to a new branch

```
git checkout -b [my-development-branch]
```

5. Make your changes
6. Add and commit your changes to your branch

```
git add .  # all changes or specify file names
git commit -m "Add a commit message here"
```

7. Push your changes to your fork

```
git push origin [my-development-branch]
```

8. Go back to your forked repo in the browser
9. Click on the message saying "Compare & pull request"

![Compare & pull request message](https://github.com/Code-Institute-Community/ci-hackathon-app/blob/forking-md/static/img/documentation/compare-and-pull.PNG?raw=true)

10. Make sure that the Pull Request is to the 