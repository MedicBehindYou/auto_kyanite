# auto_kyanite

Original program here: https://gitlab.com/lu-ci/kyanite

Docker container only, no automation: https://github.com/MedicBehindYou/docker_kyanite

Docker Hub: https://hub.docker.com/r/medicbehindyou/auto_kyanite

## Description

WARNING: This is all alpha stuff, please follow common sense when using this application.

Kyanite is a tool for scraping certain sites, and auto_kyanite is a python script that wraps Kyanite to perform that task automatically. If you only want to scrape every so often, or only have one or two tags you are interested in, I would suggest using [**Docker_Kyanite**](https://github.com/MedicBehindYou/docker_kyanite) instead. 

Auto_Kyanite utilizes an SQL Lite DB to store your tags and then runs kyanite itself against it. The problem that caused me to start this project is that these websites will rate limit you, and if they do, Kyanite sometimes doesn't recover. Also running 10 Kyanite containers at once was a drain on my server. Auto_Kyanite solves both of these by introducing an adjustable inactivity checker, and the ability to just let it run without monitoring it. It also solves the problem of noting when you last ran a tag or keeping track of everything you want to keep up to date. Auto_Kyanite is not perfect by any stretch of the imagination, but it sure beats manually doing this. So if you're a data hoarder like me, I hope this helps!

## Setup Instructions 

### -Build Yourself

1. First you will need to create the container:

    gh repo clone MedicBehindYou/docker_kyanite
    cd docker_kyanite/
    docker build .

2. This will create a local container with a random name, you can then run the container with the command example in the Docker.run file adding the name of the new container to the end. Example (Please use the command in the Docker.run file as that will have the most up-to-date syntax):

    docker run --rm -d --init --name "auto_kyanite" -e TZ=Your/TimeZone -v "/path/tp/downloads:/app/downloads:rw" -v "/path/to/config:/config:rw" container_name --any_switches

3. Run the container with the --setup switch to create the DB, and run --bulk to import your tags. Then if you care that they download in alphabetical order like I do, run --organize.

4. To start downloading, run with no switches.

5. Presto, you should be automatically downloading your selected tags.

### -Pull From Docker Hub

1. First decide what tag you want to use:
    - thiccc: Prebuilt latest with no size reduction applied. Approximately 450 MB compressed and 1.1 GB uncompressed.
    - latest: The latest slim image. Approximately 150 MB compressed and 500 MB uncompressed.
    - vX.X.X: Older versions of latest.

2. Now that you've decided, go ahead and pull the image:

    docker pull medicbehindyou/auto_kyanite:YOUR_TAG_HERE

3. You can now run the container with the latest run command, i.e.:

    docker run --rm -d --init --name "kyanite_db" -e TZ=America/Chicago -v "/mnt/user/Data/Plex/photos:/app/downloads:rw" -v "/mnt/user/Docker/kyanite_db:/config:rw" medicbehindyou/auto_kyanite:latest --any_switches

4. Run the container with the --setup switch to create the DB, and run --bulk to import your tags. Then if you care that they download in alphabetical order like I do, run --organize.

## Switches

| Switch | Description |
| :----- | :---------- |
| --setup | Creates the "database.db" file for the program to use. |
| --bulk | By default imports all tags in the file '/config/entries.txt' but can be run with a custome filepath. |
| --single | Imports a single tag, i.e. --single "a,tag,you,want" |
| --organize | Alphabetizes the tags from A-Z in the DB. |
| --uncensor | Creates a list of tags that do not contain ",uncensored" and do not have a counterpart with ",uncensored" and adds the tags to the DB with ",uncensored" appended. |

## Known Issues

- If you are seeing "OS Error" in your runs, check if you have anything other than the folders Kyanite generates in your /App/Download mount as that breaks Kyanite itself.

- If you update your image, you may need to manually update your config.ini file as Docker will respect your version over the one it has.