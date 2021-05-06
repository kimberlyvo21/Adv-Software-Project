# project-a-09

Exercise Gamification has been made to help bring people towards exercising after/during Covid-19 by making it more game-like through features like leveling and badges. The levels and badges you earn by completing workouts that you have assigned yourself can be compared with other people that you have added as friends to get a sense of community after the long quarantine and/or isolation caused by Covid-19.

The app runs on heroku-django, travis-ci, PostgreSQL database, Google Login, and other dependencies that can be found under the requirements.txt and requirements-travis.txt files. The .travis.yml file contains the settings required for the travis-ci to work and check the code before it is deployed automatically onto Heroku. The app also uses a Youtube API where settings for that can be found under the settings.py folder, alongside other information about the database's settings and the host servers for the web app that is allowed to run the app on. In order to access the database and edit user information as an admin, a superuser will need to be created. A virtual environment will also be required to run this web app on your local server. The env folder can provide information about this, along with Youtube API, Google Login, and other feature packages that will be required.

Resources for the project can be found in the various files where outside resources were used. The main resources used were the Django Polls tutorial, Bootstrap documentation, and Python Documentation, where more specific links and other resources can be found in the files.

Below one can see a general overview of the Exercise Gamification App and what each of the different tabs have in store for the user.
---------------------------------------------------------------------

LOGIN:
Users can login with their Google Email account through the Google API.

After logging in, new users can then set the username of their profile, and
also input their age and height, following by all users being directed to the 
Profile page.

---------------------------------------------------------------------

PROFILE:
Within the profile page, the user can see personal statistics such
as Age, Height, Current Badge and Level. 

Every 5 levels, the user can earn a new badge in the following order: 
Bronze, Silver, Gold, Diamond. These badges were custom made!

Levels can be increased by the converted score system of completing 
minutes of a workout.

---------------------------------------------------------------------

DASHBOARD:
The dashboard page displays Current Workouts, Progress on Workouts,
and Friends.

The User can create new workouts and set a name and goal. The workout
can then be updated with minutes accomplished by the user. As a result,
the progress bar will be increased proportionally.

When the goal is completed, both the workout and progress bar will be 
removed from the dashboard and points will be updated.

Users can add friends (try adding "hayden" or "kimberly) and the friends
list will be updated with the newly added friends.

---------------------------------------------------------------------

LEADERBOARD:
The leaderboard page displays the user's friends and their respective 
level and likes. Other users can increase the likes of friends by 
checking the button and clicking the desired friend's name.

Friends will be ranked by the level of the user in descending order.

---------------------------------------------------------------------

WORKOUTS:

The workout page displays a Youtube search engine that allows users to
view the top three searches of a workout. In addition, users can access
their workouts and update their progress or create new workouts.
