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

On the server side we decided to implement the following API on Python.
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

For the client we choose to ...



## Tests and PoC



## Summary
