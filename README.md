# CI Hackathon App

## Contributing

This project is a community effort, and everyone is welcome to contribute!

Please see the **[Contribution Guidelines](CONTRIBUTING.md)** for more information.

We are also pleased to accept PRs during the **[Hacktoberfest 2020](https://hacktoberfest.digitalocean.com/) Event**!

---

## Design

For information about **Framework**, **Color Scheme**, **Icons**, and **Typography**, please refer to the **[Design Wiki](https://github.com/Code-Institute-Community/ci-hackathon-app/wiki/Design)**.

---

## Development

Full details can be found on the **[Contribution Guidelines](CONTRIBUTING.md)** and/or the **[Development Wiki](https://github.com/Code-Institute-Community/ci-hackathon-app/wiki/Development)** pages.

Please ensure development is done within a *virtual environment*, whether locally or on Gitpod.

Our current preference is to have contributors work directly in **Gitpod**, to avoid any possible implications that may arise from not using a virtual environment.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Code-Institute-Community/ci-hackathon-app)

In order to run this project locally on your own system, you will need the following installed (as a bare minimum):

- [Python3](https://www.python.org/downloads) to run the application.
- [PIP](https://pip.pypa.io/en/stable/installing) to install all app requirements.
- [GIT](https://www.atlassian.com/git/tutorials/install-git) for cloning and version control.
- [Microsoft Visual Studio Code](https://code.visualstudio.com) (*or any suitable IDE*).

Next, there's a series of steps to take in order to proceed with local deployment:

- Clone this GitHub repository by clicking the green "*Code*" button above, in order to [download the project as a zip-file](https://github.com/Code-Institute-Community/ci-hackathon-app/archive/master.zip) (*remember to unzip it first*), or by entering the following command into the Git CLI terminal:
    - `git clone https://github.com/Code-Institute-Community/ci-hackathon-app.git`
- Navigate to the root directory after unpacking the files.
    - `cd <path to root directory>`
- Create a `.env` file with the specified variables.
    - `touch .env`
    - View our example [.env_sample](.env_sample) file for reference.
- Install all requirements from the [requirements.txt](requirements.txt) file:
    - `pip3 install -r requirements.txt`
- Launch the Django project:
    - `python3 manage.py runserver`
- The Django server should be running (either locally, or on Gitpod).
- When you run the Django server for the first time, it should create a new *SQLite3* database file: **db.sqlite3**
- Stop the app with `CTRL+C`, and make sure you checkout into an appropriate **branch**. Never develop or attempt to push onto the **master** branch; this will be rejected.
    - `git branch -a` (*view existing branches*)
    - `git checkout -b new_branch_name` (*create new branch*)
    - `git checkout branch_name` (*checkout to existing branch*)
- Make sure to pull any updates from the **master** branch onto the current branch:
    - `git pull origin master`
- Next, you will need to make migrations to create the database schema:
    - `python3 manage.py makemigrations`
    - `python3 manage.py migrate`
- In order to access the Django *Admin Panel*, you must generate a superuser:
    - `python3 manage.py createsuperuser`
    - (assign your own admin *username*, *email*, and *secure password*)
- Launch the Django project once again:
    - `python3 manage.py runserver`

Once the database migrations and superuser have been successfully completed, Django should migrate the existing `migrations.py` files from each app to configure the following relational schema:

*(NOTE: this is not the actual schema yet, and will be updated soon.)*

![flow-chart](static/img/flow-chart.png?raw=true "flow-chart")

- Once you're happy with all changes, you can commit and push your code to the appropriate branch:
    - `git add <files>`
    - `git commit -m "Your commit message"`
    - `git push origin <BRANCH_NAME>`
    - *reminder: do **not** attempt to push to the **master** branch!*
- Finally, you will need to open a [Pull Request](https://github.com/Code-Institute-Community/ci-hackathon-app/pulls) on GitHub, detailing all required information:
    - What specific changes are you requesting?
    - What impact will these changes make to the project?
    - Are there any known bugs/issues remaining with these changes?
        - *please try to fix these before submitting a PR*
    - Any additional context necessary for the code review.

Happy Coding, and thanks for Contributing to the Code Institute Community!

---

## Technologies

For information about **Front-End** and **Back-End** Technologies, please refer to the **[Technologies Wiki](https://github.com/Code-Institute-Community/ci-hackathon-app/wiki/Technologies)**.

---

## Testing

For more information about **Code Validation**, **Compatibility**, and **Automated Testing**, please refer to the **[Testing Wiki](https://github.com/Code-Institute-Community/ci-hackathon-app/wiki/Testing)**.

---

## User Stories

For information about **User Stories**, please refer to the **[User Stories Wiki](https://github.com/Code-Institute-Community/ci-hackathon-app/wiki/User-Stories)**.

---

## Wireframes

For information about **Wireframes**, please refer to the **[Wireframes Wiki](https://github.com/Code-Institute-Community/ci-hackathon-app/wiki/Wireframes)**

---

## Acknowledgements

We appreciate all contributions, and want to give a special thanks to everyone involved!

- [Tim Nelson](https://github.com/TravelTimN)
- [Stefan Dworschak](https://github.com/stefdworschak)

---

## License

Full License and Copyright details can be found under the [MIT LICENSE](LICENSE) unless specified otherwise.
