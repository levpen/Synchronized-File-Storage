#  Synchronized-File-Storage project report

## Tasks of the project

### Project overwiev

Our project will represent a remote server with which we can synchronize files (downoad and upload). Basic functionality include uploading, deleting and downloading data to and from the server.

### Resposibilities

- Dzhovidon Vakhidov (starkda) - docker configuraion
- Bulat Kutlugallyamov (bulatok) - client
- Anton Sokrkin (Antony-Sk) - server
- Lev Gorbunkov (levpen) - report

## Execution steps

On the server side we decided to implement the following API.
### Server API
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

For the client we choose the following API:
### Client API:
- setup - setep the client for use

- sync - syncs data from server

  Arguments:
  - -d: Argument for date_from
  - -dirs(optional): Argument for dirs
- info - list config data
- push - push data onto the server

  Arguments:
  - file_names - files to push to the server
- delete - delete data from server

  Arguments:
  - file_names - files to delete from the server



## Tests and PoC

To test the code we made the docker image which starts several clients and runs some commands. We also used linter with flake8 integrated in GitHub Actions for CI/CD.



## Summary

In summary, we realized what we wanted, but our project still can be improved in many ways. For future improvements we could add merging conflicts resolution.
