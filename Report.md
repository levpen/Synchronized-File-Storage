#  Synchronized-File-Storage project report

## Tasks of the project

### Project overwiev

Our project will represent a remote server with which we can synchronize files (downoad and upload). Basic functionality include uploading, deleting and downloading data to and from the server.

### Resposibilities

- Dzhovidon Vakhidov (starkda) - docker configuraion
- Bulat Kutlugallyamov (bulatok) - client
- Anton Sokrkin (Antony-Sk) - server
- Lev Gorbunkov (levpen) - report, GH Actions

## Execution steps
Our project has a server-client architecture, so we divided the server and client parts.

### Server part
Firstly, the server starts from the server.py on the ```http://127.0.0.1:8000```. It saves the data into the ```./storage``` and also contains history in binary format inside ```.history``` file. On the server side we decided to implement the following API.
#### Server API
- GET: /get_since - returns files since the date argument
  
  Params:
  - date: date-time (timestamp) from which the client wants to get new data 
  - dir (optional): a subdirectory for synchronization (if the client only wants to pull up its changes)
- DELETE: /delete - deletes needed file
  
  Params:
  - name: the name of the file to be deleted
- POST:/post - saves file with given name
  
  Params:
  - file: binary data of the file
  - name: the full name of the file from the root of the synchronized directory

### Client part
The client always starts from the ```main.py```. When we first start the client we should initiate the setup with ```main.py setup``` command. This command saves the url address of the server into the ```config.json```. Next we can operate with the client via ```sync```, ```push```, or ```delete``` commands.
For the client we choose the following API:
#### Client API:

optional arguments:
  - -h, --help            show this help message and exit
  - -v, --verbose         Enable verbose output
 
 Commands: 

- setup - setep the client for use
- info - shows config data inside ```config.json```

- sync - syncs data from server

  Arguments:
  - -d: Argument for date_from (e.g. ```-d '2022 year'```)
  - -dirs(optional): Argument for dirs
- push - push data onto the server

  Arguments:
  - file_names - files to push to the server
- delete - delete data from server

  Arguments:
  - file_names - files to delete from the server

Also our client can be used as Debain package. To make it work user need write command
```bash
  $ make package
```

Now user can just write something like
```
  $ sfsclient COMMAND
```
where commands are sync, push, setup, info ... with all flags.




## Tests and PoC

To test the code we made the docker image which starts several clients and runs some commands. We also used linter with flake8 integrated in GitHub Actions for CI/CD.

### Demo: https://www.youtube.com/watch?v=TqQ26icdvks

## Difficulties faced
During the work on our project we managed to develop the working version of the product after long period of debugging and rechecking. In overall, we learned to communicate in command properly, distribute the work over each team member, and learned many technical skills.

## Summary

In summary, we realized what we wanted, but our project still can be improved in many ways. For future improvements we could add merging conflicts resolution and other file formats besides txt.
