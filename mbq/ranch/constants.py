from common.constants import ChoicesBase


class TaskStatus(ChoicesBase):
    FAILURE = 'FAILURE'
    REJECTED = 'REJECTED'
    UNKNOWN = 'UNKNOWN'
