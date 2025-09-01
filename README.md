# GitLab Contribution Mirror

Hello! If you've landed on this repository, you've probably noticed its rather peculiar commit history. This project serves as a dynamic mirror of my professional activity, which primarily takes place in a private GitLab environment.

## 🎯 The Goal

As a developer, my GitHub profile serves as a professional showcase. However, my daily work and most consistent contributions happen on a corporate GitLab server, which is not public. This resulted in a contribution graph on my profile that didn't reflect my actual engagement and work consistency.

## 💡 The Solution

This repository uses GitHub Actions to populate my profile's contribution graph. The solution is designed to be completely secure and to respect the confidentiality of the professional environment.

The process works as follows:

1.  Daily Execution: An automated routine (workflow) runs every day.
2.  Metadata Collection: A Python script connects to my company's GitLab API using a secure access token. It only reads metadata about my activities (commits, merge requests, comments, etc.), never accessing the code itself.
3.  Creation of Empty Commits: For each day that had at least one activity on GitLab, the script creates a corresponding empty commit in this repository. The commit message is dynamically generated to summarize the types of contributions for that day (e.g., `GitLab activity on 2025-09-01 (pushed, commented)`).
4.  Synchronization: The new commits are pushed to this repository, and GitHub uses them to fill in the squares on my profile graph.

The result is a faithful, daily representation of my dedication and work, transforming a once-static profile into an accurate reflection of my day-to-day life as a developer.
