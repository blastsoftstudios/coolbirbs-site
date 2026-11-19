# coolbirbs-site

Static build of [coolbirbs.com](https://coolbirbs.com), hosted on GitHub Pages.

`build.py` renders one page per bird seed (0-9999) into `dist/` using the stdlib-only
name generator in `birdgenerator/`. Names are deterministic per seed, so permalinks and
Open Graph tags are identical to the old Django site. Bird images are served from
`static.coolbirbs.com`, not this repo.

    python3 build.py
    python3 -m http.server -d dist

Pushes to `master` build and deploy via `.github/workflows/pages.yaml`.
