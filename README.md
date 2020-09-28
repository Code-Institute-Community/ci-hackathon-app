# CI Hackathon App

---

## Table of Contents
1. [**Contributing**](#contributing)

2. [**UX**](#ux)
    - [**User Stories**](#user-stories)
    - [**Design**](#design)
        - [**Framework**](#framework)
        - [**Color Scheme**](#color-scheme)
        - [**Icons**](#icons)
        - [**Typography**](#typography)
    - [**Wireframes**](#wireframes)

3. [**Features**](#features)
    - [**Existing Features**](#existing-features)
    - [**Features Left to Implement**](#features-left-to-implement)

4. [**Technologies Used**](#technologies-used)
    - [**Front-End Technologies**](#front-end-technologies)
    - [**Back-End Technologies**](#back-end-technologies)

5. [**Testing**](#testing)
    - [**Validators**](#validators)
    - [**Compatibility**](#compatibility)
    - [**Automated Testing**](#automated-testing)

5. [**Deployment**](#deployment)
    - [**Local Deployment**](#local-deployment)

7. [**Credits**](#credits)
    - [**Content**](#content)
    - [**Media**](#media)
    - [**Code**](#code)
    - [**Acknowledgements**](#acknowledgements)

8. [**License**](#license)

---

## Contributing

This project is a community effort, and everyone is welcome to contribute!

Please see the [Contribution Guidelines](CONTRIBUTING.md) for more information.

We are also pleased to accept PRs during the [Hacktoberfest 2020](https://hacktoberfest.digitalocean.com/) Event!

##### back to [top](#table-of-contents)

---

## UX

TBD

### User Stories

- [x] *successfully implemented*
- [ ] *not yet implemented*

"**_As a Student, I would like to_** _______________"

- [ ] User Story (student) #1.
- [ ] User Story (student) #2.
- [ ] User Story (student) #3.

"**_As CI Staff, I would like to_** _______________"

- [ ] User Story (staff) #1.
- [ ] User Story (staff) #2.
- [ ] User Story (staff) #3.

### Design

TBD

#### Framework

- [Bootstrap 4.5.x](https://getbootstrap.com/)

#### Color Scheme

*Palette*: **Primary Colors**

| `--p-orange` | `--p-blue` | `--p-grey` | `--p-navy` | `--p-red` |
| :---: | :---: | :---: | :---: | :---: |
| ![#E84610](https://placehold.it/15/E84610/E84610) | ![#009FE3](https://placehold.it/15/009FE3/009FE3) | ![#4A4A4F](https://placehold.it/15/4A4A4F/4A4A4F) | ![#445261](https://placehold.it/15/445261/445261) | ![#D63649](https://placehold.it/15/D63649/D63649) |
| #E84610 | #009FE3 | #4A4A4F | #445261 | #D63649 |

*Palette*: **Secondary Colors**

| `--s-grey` | `--s-yellow` | `--s-pink` | `--s-teal` |
| :---: | :---: | :---: | :---: |
| ![#E6ECF0](https://placehold.it/15/E6ECF0/E6ECF0) | ![#EFB920](https://placehold.it/15/EFB920/EFB920) | ![#FF5A60](https://placehold.it/15/FF5A60/FF5A60) | ![#23BBBB](https://placehold.it/15/23BBBB/23BBBB) |
| #E6ECF0 | #EFB920 | #FF5A60 | #23BBBB |

*Palette*: **Tertiary Colors**

| `--t-grey` |
| :---: |
| ![#E0E7FF](https://placehold.it/15/E0E7FF/E0E7FF) |
| #E0E7FF |

**CSS Color `:root` Variables**

```css
:root {
    /* P = Primary | S = Secondary | T = Tertiary */
    --p-orange: #E84610;
    --p-blue: #009FE3;
    --p-grey: #4A4A4F;
    --p-navy: #445261;
    --p-red: #D63649;
    --s-grey: #E6ECF0;
    --s-yellow: #EFB920;
    --s-pink: #FF5A60;
    --s-teal: #23BBBB;
    --t-grey: #E0E7FF;
    --bg-grey: #F5F5F5;
}

/* How To Use CSS Root Variables */
element {
    color: var(--p-orange);
    background-color: var(--bg-grey);
}
```

#### Icons

- [Font Awesome 5.14](https://fontawesome.com/)
    - Library of all Font Awesome version 5 [free icons](https://fontawesome.com/icons?d=gallery&m=free).

#### Typography

- [Montserrat](https://fonts.google.com/specimen/Montserrat) : primary font-family, with `sans-serif` fallback.
- [Rubik](https://fonts.google.com/specimen/Rubik) : secondary font-family, with `sans-serif` fallback.

### Wireframes

TBD

##### back to [top](#table-of-contents)

---

## Features

TBD

### Existing Features

- TBD

### Features Left to Implement

- TBD

##### back to [top](#table-of-contents)

---

## Technologies Used

- TBD

### Front-End Technologies

- ![HTML](https://img.shields.io/static/v1?label=HTML&message=5&color=E34F26&logo=html5&logoColor=ffffff)
    - [HTML](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) - Used as the base for markup text.
- ![CSS](https://img.shields.io/static/v1?label=CSS&message=3&color=1572B6&logo=css3&logoColor=ffffff)
    - [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3) - Used as the base for cascading styles.
- ![jQuery 3.5](https://img.shields.io/static/v1?label=jQuery&message=3.5&color=0769AD&logo=jquery&logoColor=ffffff)
    - [jQuery 3.5](https://code.jquery.com/jquery/) - Used as the primary JavaScript functionality with Bootstrap.
- ![Bootstrap 4.5](https://img.shields.io/static/v1?label=Bootstrap&message=4.5&color=563d7c&logo=bootstrap&logoColor=ffffff)
    - [Bootstrap 4.5](https://getbootstrap.com/) - Used as the front-end framework for layout and design.

### Back-End Technologies

- ![Python](https://img.shields.io/static/v1?label=Python&message=3.6.8&color=blue&logo=python&logoColor=ffffff)
    - [Python 3.6.8](https://www.python.org/) - Used as the back-end programming language.
- ![Django](https://img.shields.io/static/v1?label=Django&message=3.1.1&color=092E20&logo=django)
    - [Django 3.1.1](https://docs.djangoproject.com/en/3.1/) - Used as the Python web framework.
- ![django-allauth](https://img.shields.io/static/v1?label=django-allauth&message=0.42.0&color=2980B9)
    - [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) - Used for user authentication with Django.
- ![django-forms-bootstrap](https://img.shields.io/static/v1?label=django-forms-bootstrap&message=3.1.0&color=563d7c)
    - [django-forms-bootstrap](https://pypi.org/project/django-forms-bootstrap/) - Used for simple Bootstrap forms with Django.

##### back to [top](#table-of-contents)

---

## Testing

TBD

### Validators

**HTML**
- [W3C HTML Validator](https://validator.w3.org)

**CSS**
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)

**JavaScript**
- [JShint](https://jshint.com/)

**Python**
- [PEP8 Online](http://pep8online.com/)

### Compatibility

TBD

- **Chrome**
- **Edge**
- **Firefox**
- **Safari**
- **Opera**
- **Internet Explorer**

### Automated Testing

TBD

##### back to [top](#table-of-contents)

---

## Deployment

### Local Deployment

Please ensure development is done within a *virtual environment*, whether locally or on Gitpod.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Code-Institute-Community/ci-hackathon-app)

In order to run this project locally on your own system, you will need the following installed (as a bare minimum):

- [Python3](https://www.python.org/downloads) to run the application.
- [PIP](https://pip.pypa.io/en/stable/installing) to install all app requirements.
- [GIT](https://www.atlassian.com/git/tutorials/install-git) for cloning and version control.
- [Microsoft Visual Studio Code](https://code.visualstudio.com) (*or any suitable IDE*).

Next, there's a series of steps to take in order to proceed with local deployment:

- Clone this GitHub repository by clicking the green "*Code*" button above, in order to [download the project as a zip-file](https://github.com/Code-Institute-Community/ci-hackathon-app/archive/master.zip) (*remember to unzip it first*), or by entering the following command into the Git CLI terminal:
    - `git clone https://github.com/Code-Institute-Community/ci-hackathon-app.git`
- Navigate to the correct file location after unpacking the files.
    - `cd <path to folder>`
- Create a `.env` file with the specified variables.
    - `touch .env`
    - The example *.env* file can be found here ([.env_sample](.env_sample)).
- Install all requirements from the [requirements.txt](requirements.txt) file:
    - `pip3 install -r requirements.txt`
- Launch the Django project:
    - `python3 manage.py runserver`
- The Django server should be running (either locally, or on Gitpod).
- When you run the Django server for the first time, it should create a new *SQLite3* database file: **db.sqlite3**
- Stop the app with `Ctrl+C`, and make sure you checkout into an appropriate **branch**. Never develop or attempt to push onto the **master** branch, this will be rejected.
    - `git branch -a` (*view existing branches*)
    - `git checkout -b new_branch_name` (*create new branch*)
    - `git checkout branch_name` (*checkout to existing branch*)
- Next, you will need to make migrations to create the database schema:
    - `python3 manage.py makemigrations`
    - `python3 manage.py migrate`
- In order to access the Django *Admin Panel*, you must generate a superuser:
    - `python3 manage.py createsuperuser`
    - (assign an admin username, email, and secure password)
- Launch the Django project once again:
    - `python3 manage.py runserver`

Once the database migrations and superuser have been successfully completed, Django should migrate the existing `migrations.py` files from each app to configure the following relational schema:

![flow-chart](static/img/flow-chart.png?raw=true "flow-chart")

##### back to [top](#table-of-contents)

---

## Credits

### Content

- [Shields.io](https://shields.io) - Used to create markdown badges on the README.

### Media

- []()
- []()

### Code

- []()
- []()

### Acknowledgements

- [Tim Nelson](https://github.com/TravelTimN)
- [Stefan Dworschak](https://github.com/stefdworschak)

---

## License

Full License and Copyright details can be found under the [MIT LICENSE](LICENSE) unless specified otherwise.

##### back to [top](#table-of-contents)
