class ServerStatus:
    online_users: int
    maintenance: bool
    total_users: int
    scores_submitted: int
    def __init__(self):
        self.online_users = 0
        self.maintenance = False
        self.total_users = 0
        self.scores_submitted = 0