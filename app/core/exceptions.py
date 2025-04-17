from typing import Any


class AlreadyExistsError(Exception):
    def __init__(self, entity: str, identifier: str, value: Any):
        self.entity = entity
        self.identifier = identifier
        self.value = value
        super().__init__(f'{self.entity} with {self.identifier} = {self.value} already exist')
    
class NotFoundError(Exception):
    def __init__(self, entity: str = None, identifier: str = None, value: Any = None, error_message: str = None):
        self.entity = entity
        self.identifier = identifier
        self.value = value
        if not error_message:
            error_message = f'{self.entity} with {self.identifier} = {self.value} not found'
        if not self.value and not self.identifier:
            error_message = f'{self.entity} not found'
        super().__init__(error_message)
    
class CredentialsError(Exception):
    def __init__(self):
        error_message = f'Could not validate credentials'
        super().__init__(error_message)
        