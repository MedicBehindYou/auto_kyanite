# auto_kyanite

# TODO: #1 Create an entries binding, or switch to having everything in one folder. May need to recreate Docker Run command then. Fix steps marked with IMPROVE. Right now, the database.db needs to already exist, which isn't ideal.

Original program here: https://gitlab.com/lu-ci/kyanite

Docker container only: https://github.com/MedicBehindYou/docker_kyanite

## Description

WARNING: This is all alpha stuff, please follow common sense when using this application.

Kyanite is a tool for scraping certain sites, and auto_kyanite is a python script that wraps Kyanite to perform that task automatically. If you only want to scrape every so often, or only have one or two tags you are interested in, I would suggest using [**Docker_Kyanite**](https://github.com/MedicBehindYou/docker_kyanite) instead. 

Auto_Kyanite utilizes an SQL Lite DB to store your tags and then runs kyanite itself against it. The problem that caused me to start this project is that these websites will rate limit you, and if they do, Kyanite sometimes doesn't recover. Also running 10 Kyanite containers at once was a drain on my server. Auto_Kyanite solves both of these by introducing an adjustable inactivity checker, and the ability to just let it run without monitoring it. It also solves the problem of noting when you last ran a tag or keeping track of everything you want to keep up to date. Auto_Kyanite is not perfect by any stretch of the imagination, but it sure beats manually doing this. So if you're a data hoarder like me, I hope this helps!

## Setup Instructions

1. First you will need to create the container:

    gh repo clone MedicBehindYou/docker_kyanite
    cd docker_kyanite/
    docker build .

2. This will create a local container with a random name, you can then run the container with the command example in the Docker.run file adding the name of the new container to the end. Example (Please use the command in the Docker.run file as that will have the most up-to-date syntax):

    docker run --rm -d --init --name "auto_kyanite" -e TZ=Your/TimeZone -v "/path/tp/downloads:/app/downloads:rw" -v "/path/to/database.db:/app/database.db:rw" -v "/path/to/log.txt:/app/log.txt:rw" -v "/path/to/backup:/app/backup:rw" container_name --any --switches

3. IMPROVE: Run the container with the --setup switch to create the DB, and run --bulk to import your tags. Then if you care that they download in alphabetical order like I do, run --organize.

4. To start normally, run with no switches.

5. Presto, you should be automatically downloading your selected tags.

## IMPROVE: Switches

| Switch | Description |
| :----- | :---------- |
| --setup | Creates the "database.db" file for the program to use. |