import subprocess

output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf', 'release_note.docx'])
