from app.repositories.expected_worker_repository import ExpectedWorkerRepository


class ExpectedWorkerService:
    def __init__(self):
        self.repo = ExpectedWorkerRepository()

    def get_all_by_company(self, organization_name: str):
        return self.repo.get_all_by_company(organization_name)
