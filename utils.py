import os

# Authenticate and link to google drive
def auth():
  os.system('!apt-get install -y -qq software-properties-common python-software-properties module-init-tools')
  os.system('!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null')
  os.system('!apt-get update -qq 2>&1 > /dev/null')
  os.system('!apt-get -y install -qq google-drive-ocamlfuse fuse')
  
  from google.colab import auth
  auth.authenticate_user()
  
  from oauth2client.client import GoogleCredentials
  creds = GoogleCredentials.get_application_default()
  
  import getpass
  os.system('!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL')
  vcode = getpass.getpass()
  os.system('!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}')

def save_all(filename):
  # tar all files in current directory
  os.system('!tar -cvf 'filename' .')
  
  # save to drive
  from googleapiclient.http import MediaFileUpload
  from googleapiclient.discovery import build

  auth.authenticate_user()
  drive_service = build('drive', 'v3')

  def save_file_to_drive(name, path):
    file_metadata = {'name': name, 'mimeType': 'application/octet-stream'}
    media = MediaFileUpload(path, mimetype='application/octet-stream', resumable=True)
    created = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return created

  save_file_to_drive(filename, filename)
