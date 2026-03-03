# Contributing to Jarvis AI

Thank you for your interest in contributing to Jarvis AI! This guide explains how to submit changes and how pull requests are reviewed and approved.

## How to Submit a Pull Request

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:

        git clone https://github.com/<your-username>/myPA-AI-Python.git

3. **Create a branch** for your changes:

        git checkout -b feature/your-feature-name

4. **Make your changes** and commit them with a clear message:

        git commit -m "Add: brief description of your change"

5. **Push** your branch to your fork:

        git push origin feature/your-feature-name

6. Open a **Pull Request** against the `main` branch of this repository on GitHub.

## How to Approve a Pull Request

Pull request approval is performed by repository maintainers on GitHub. Here is the process:

1. **Navigate** to the repository on GitHub and click the **Pull requests** tab.
2. **Open** the pull request you want to review.
3. Click the **Files changed** tab to review the diff.
4. Leave inline comments on specific lines if needed by clicking the **+** icon next to a line.
5. When you are satisfied with the changes, click the **Review changes** button (top right of the Files changed view).
6. Select one of the following options:
   - **Comment** – Submit general feedback without explicitly approving or requesting changes.
   - **Approve** – Approve the pull request. The author can merge once all required approvals are collected.
   - **Request changes** – Ask the author to make further changes before the PR can be merged.
7. Click **Submit review** to finalize your review.
8. Once all required approvals are in place and any CI checks pass, the PR can be **merged** by clicking the **Merge pull request** button.

## Code Style Guidelines

- Follow standard Python conventions ([PEP 8](https://peps.python.org/pep-0008/)).
- Keep functions focused and well-named.
- Add comments to explain non-obvious logic.
- Update `requirements.txt` if you add new dependencies.

## Reporting Issues

If you find a bug or want to suggest a new feature, please [open an issue](../../issues) with a clear description of the problem or idea.
