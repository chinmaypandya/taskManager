class RequestException(Exception):
    def __init__(self, message: str, status_code: int, hint: str):
        self.message = message
        self.status_code = status_code
        self.hint = hint

class CustomException(Exception):
    def __init__(self, message, status_code, hint):
        self.message = message
        self.status_code = status_code
        self.hint = hint

InvalidApiKeyException = RequestException('Invalid API key', 401, 'Your API key has either expired or incorrect. Try renewing your key')
NoLoginException = RequestException('User has not logged In', 401, 'You need to login to start a session, some features are limited to logged in users only')

UserNotFoundException = RequestException('User does not exist', 404, 'Your data is already deleted or was never created')
TeamNotFoundException = RequestException('Team does not exist', 404, 'The team is already deleted or was never created')
TaskNotFoundException = RequestException('Task does not exist', 404, 'The task is already deleted or was never created')
RequestNotFoundException = RequestException('Request does not exist', 404, 'The request is already deleted/accepted or was never created')

NoAccessException = RequestException('You do not have access', 403, 'This is a private feature not open to all users. Try logging in with classified credentials')

InvalidPasswordException = RequestException('Invalid Credentials', 400, 'Your information does not match the documents in the database')

SessionException = RequestException('A session is ongoing, logout first', 409, 'You need to logout first in order to start another session')
UserAlreadyExistsException = RequestException('User already exists', 409, 'Cannot create a new user, Your data already exists for the action')
RequestAlreadyExistsException = RequestException('Join Request already exists', 409, 'Cannot create a new request, Please wait till it is either rejected/accepted')
TeamAlreadyExistsException = RequestException('Team already exists', 409, 'Cannot create a new team with the same code. Try deleting the previous one')
TaskAlreadyExistsException = RequestException('Task already exists', 409, 'Cannot create a new task, Try deleting the old one or wait for user to complete it')