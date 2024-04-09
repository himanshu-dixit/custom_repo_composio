import unittest
from create_issue import CreateIssueRequest, CreateLinearIssue

class TestCreateIssue(unittest.TestCase):
    def setUp(self):
        self.create_issue_action = CreateLinearIssue()
        self.authorisation_data = {"headers": {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}}
        self.test_cases = [
            {
                "name": "test_create_issue_success",
                "request": CreateIssueRequest(
                    project_id="valid_project_id",
                    issue_title="Test Issue",
                    description="This is a test issue",
                    team_id="valid_team_id"
                ),
                "expected": {"executed": True, "contains_error": False}
            },
            {
                "name": "test_create_issue_failure",
                "request": CreateIssueRequest(
                    project_id="invalid_project_id",
                    issue_title="",
                    description="",
                    team_id="invalid_team_id"
                ),
                "expected": {"executed": False, "contains_error": True}
            }
        ]

    def test_create_issue(self):
        for case in self.test_cases:
            with self.subTest(case["name"]):
                response = self.create_issue_action.execute(case["request"], self.authorisation_data)
                if case["expected"]["executed"]:
                    print(response)  # Assuming print is for debug/logging
                else:
                    self.assertFalse(response["execution_details"]["executed"])
                    if case["expected"]["contains_error"]:
                        self.assertIn("error", response["response_data"])

if __name__ == '__main__':
    unittest.main()

