# Contributing

Thank you for taking the time to contribute! This profile repository is automatically refreshed by a GitHub Actions workflow that updates the Projects section in `README.md`. The workflow calls `scripts/update_projects.py`, which queries the GitHub API and rebuilds the list of projects. Repositories are ranked based on whether they carry the `featured` topic, how recently they were updated, and their star count. If the generated content differs from the current README, the workflow uses the [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request) action to open a pull request with the updated projects list.

## Adding featured projects

To prioritise a repository in the Projects section, add the **featured** topic to that repository. Navigate to your repository’s **Settings**, find the **Topics** field and add `featured`. The next time the scheduled workflow runs (or when triggered manually) that repository will appear at the top of the list.

## Running the update manually

The workflow is scheduled to run daily and can also be triggered on demand from the **Actions** tab. Select the **Update projects** workflow and click **Run workflow**.

## Local testing

You can run the update script locally:

1. Install the dependencies:

   ```bash
   pip install PyGithub
   ```

2. Create a personal access token with `repo` scope and export it as `GH_TOKEN`:

   ```bash
   export GH_TOKEN=YOUR_TOKEN
   ```

3. Run the script from the repository root:

   ```bash
   python scripts/update_projects.py
   ```

This will update the Projects section in your local `README.md`. Commit the changes to a branch and open a pull request if necessary.

Feel free to open an issue or pull request if you have questions or ideas!
