# Working with a forked repo

## Forking the repo

In order to contribute to this project you will need to create a fork of the repo on your own account. 
To fork the repo just open the repository in a browser and click on the "fork" button on the top right of the page.

If you are part of any organisations it will ask you which organisation you want to create the fork in.
If you are not part of any, it will automatically create it under your personal GitHub account.

## Creating a Pull Request from a forked repo to the original repo

### Gitpod

1. Open your forked repo in the browser
2. Click on the GitPod button to open a new workspace
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
9. Click on the message saying "