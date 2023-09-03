from typing import Dict
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

from ..TaskBase import TaskBase

class SheetsStore(TaskBase):
  def __init__(self, form_id: str, response: Dict):
    super().__init__(form_id, response)
    self.scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    self.creds = ServiceAccountCredentials.from_json_keyfile_name(
      'tasks/SheetsStore/client_secret.json',
      scopes=self.scopes
    )
    
  def run(self):
    client = gspread.authorize(self.creds)
    self.response = sorted(self.response, key=lambda response: response['question_order'])
    
    try:
      spreadsheet = client.open(title=self.form_id)
      sheet = spreadsheet.sheet1
    except gspread.SpreadsheetNotFound:
      spreadsheet = client.create(title=self.form_id)
      sheet = spreadsheet.sheet1
      sheet.append_row(values=[resp['question_text'] for resp in self.response])
    
    sheet.append_row(values=[resp['response'] for resp in self.response])
    spreadsheet.share(value="shuvamkshah28@gmail.com", perm_type='user', role='reader')
    
    return spreadsheet.url
