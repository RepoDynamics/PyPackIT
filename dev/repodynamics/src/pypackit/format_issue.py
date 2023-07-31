# Standard libraries
import argparse
import sys


class IssueFormatter:
    def __init__(self, issue_body: str):
        self._issue_body = issue_body
        return

    def format(self):
        return """# Test
        testing 123

        ## Heading 2
        wefwefwef

        A new paragraph.

        """


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("issue_body", type=str, help="Body of the issue to format.")
    args = parser.parse_args()
    try:
        formatted_issue = IssueFormatter(issue_body=args.issue_body).format()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    print(formatted_issue)
