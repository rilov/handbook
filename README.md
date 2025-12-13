# Handbook — GitHub Pages Handbook

This repository is a small handbook site for quick tech notes, comparisons, and runbooks, designed for GitHub Pages using Jekyll.

## Structure

- `_topics/` — Add your pages here. Each file is a single topic with front matter.
- `categories/` — Category overview pages. You can add new category pages here if you want a dedicated list page.
- `_layouts/` — Jekyll layouts used to render the site.
- `assets/` — CSS and other static assets.
- `index.md` — Index page listing topics grouped by category.

## Adding a new topic

To add a new topic, create a Markdown file under `_topics` with front matter like:

```markdown
---
title: "Short descriptive title"
category: Security
tags: [tag1, tag2]
summary: Short one-line summary
---

Write your content here.
```

Commit and push to `main`; GitHub Pages will serve the site from the repository.

## Adding a new category

Create a file in the `categories` folder, set `layout: category` and set `category` frontmatter to the category name. This will use the category layout and show topics in that category.

## Local preview

This repository is intended to be published via GitHub Pages and CI. Local builds are optional and not required. Push to `main` and the repository will be built and deployed automatically using the included GitHub Actions workflow.

## Deployment

Option A — Quick publish using GitHub Pages (recommended for most users):

- Go to the repo on GitHub → Settings → Pages.
- Under 'Build and deployment' → 'Source', select 'Deploy from a branch' > Branch: `main` and Root as the folder.
- Click 'Save'. GitHub will build the site using Jekyll and the Pages feature and serve it shortly at `https://<your-username>.github.io/<repo-name>` (or `https://<your-username>.github.io` if your repo is named `<your-username>.github.io`).

Note: If you want to use a custom domain, set the "Custom domain" in the Pages settings and add a `CNAME` file at the repo root with the domain. Also add the required DNS records at your registrar.

Option B — Use a GitHub Action to build and deploy (useful if you need custom plugins or bundler versions):

- The repo includes an example workflow at `.github/workflows/pages.yml` that builds the site with Jekyll and deploys it using the official GitHub Pages actions on push to `main`.
- With this workflow, GitHub Pages will be served from the Pages deployment rather than relying on the default site build. You can use this when you use unsupported Jekyll plugins or need a specific Ruby/Jekyll version.

Option C — Host on GitHub Pages with `gh-pages` branch (alternative):

- You can still build locally if you prefer and push `_site` to a `gh-pages` branch and set Pages source to 'gh-pages branch / root' — but this is manual and usually unnecessary when using Actions.

Setting `url` and `baseurl` correctly
- If your Pages URL will be `https://<your-username>.github.io/<repo-name>` (project site), set `baseurl: "/<repo-name>"` in `_config.yml`. Example: `baseurl: "/handbook.github.io"`.
- If the site is a user/organization page (repo named `<username>.github.io`), set `baseurl: ""` and `url: "https://<your-username>.github.io"`.

Troubleshooting
- If the site looks broken or assets 404, check that `baseurl` is set correctly and that links are built with `{{ '/path' | relative_url }}` so Jekyll handles basefolder.
- If using a workflow, check the Actions tab for the build logs and artifact upload.


## Example topic

A sample topic, `Hashing vs Encryption`, is already added under `_topics`.

## Notes & Tips
- Prefer using a consistent category naming (capitalization matters in the listing code).
- For passwords, use Argon2 / bcrypt / scrypt and not fast hashes.
- Rotate keys and provide a link to the ops runbook for encryption key management.

---

Feel free to request more categories, a search box, or JS filtering if you want a richer UI.