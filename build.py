"""Render the static site into dist/ for GitHub Pages."""
import shutil
from html import escape
from pathlib import Path

from birdgenerator import generate_bird

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
SITE = 'https://coolbirbs.com'
BIRD_URL = 'https://static.coolbirbs.com/birds'
SEEDS = 10000
DEFAULT_SEED = 3818  # og:image for the home page

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-40839635-8"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());

        gtag('config', 'UA-40839635-8');
    </script>
    <title>CoolBirbs.com | this bird does not exist</title>
{meta}
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
{head_extra}</head>

<body>
    <link href="/static/font-awesome/css/fontawesome-all.min.css" rel="stylesheet">
<main role="main">

	<div class="album py-5 d-md-flex vh-100" style="background: black">
		<div class="container">

			<div class="row align-items-center h-50">
				<div class="col-lg-4 mx-auto">
					<div class="card mb-4 box-shadow bg-dark align-middle shadow-lg">
						<img class="card-img-top" src="{bird_url}/{id}.png" alt="{name}" data-holder-rendered="true" style="background: #343434; max-width: 100%; height: auto;" width="1024" height="1024">
						<div class="card-body text-center">
							<h2 class="card-title text-secondary">Cool Birb #{id}</h2>
							<p class="text-center text-light"><a href="/bird/{id}/" class="text-light"><b>{name}</b></a></p>
							<div class="d-flex justify-content-between align-items-center">
								<div class="btn-group">
									<button type="button" id="copy" data-link="{site}/bird/{id}" class="btn btn-sm btn-outline-light"><i class="far fa-copy"></i> Copy Link</button>
								</div>
								<small class="text-muted"><button type="button" class="btn btn-sm btn-outline-light" onclick="window.location.href='/'">See Another</button></small>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</main>
<script>
	document.getElementById('copy').addEventListener('click', function () {{
		navigator.clipboard.writeText(this.dataset.link);
	}});
</script>
</body>
</html>
"""

# The home page is a random bird: redirect before first paint, with the
# default bird rendered as the no-JS / crawler fallback.
RANDOM_REDIRECT = (
    '    <script>location.replace("/bird/" + Math.floor(Math.random() * %d) + "/");</script>\n' % SEEDS
)


def render(seed, permalink):
    name = generate_bird(seed)
    if permalink:
        meta = (
            '    <meta property="og:type" content="website">\n'
            '    <meta property="og:title" content="Cool Birbs" />\n'
            f'    <meta property="og:description" content="Cool Birb #{seed}: {escape(name)}" />\n'
            f'    <meta property="og:image" content="{BIRD_URL}/{seed}.png" />\n'
            f'    <meta property="og:url" content="{SITE}" />'
        )
        head_extra = ''
    else:
        meta = (
            '    <meta name="description" content="Pictures of things that may be mistaken for birds." />\n'
            '    <meta property="og:type" content="website" />\n'
            '    <meta property="og:title" content="Cool Birbs" />\n'
            '    <meta property="og:description" content="Pictures of things that may be mistaken for birds." />\n'
            f'    <meta property="og:image" content="{BIRD_URL}/{DEFAULT_SEED}.png" />\n'
            f'    <meta property="og:url" content="{SITE}" />'
        )
        head_extra = RANDOM_REDIRECT
    return PAGE.format(
        meta=meta, head_extra=head_extra, bird_url=BIRD_URL, site=SITE,
        id=seed, name=escape(name),
    )


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    write(DIST / 'index.html', render(DEFAULT_SEED, permalink=False))
    for seed in range(SEEDS):
        write(DIST / 'bird' / str(seed) / 'index.html', render(seed, permalink=True))

    shutil.copytree(ROOT / 'static', DIST / 'static')
    shutil.copy(ROOT / 'robots.txt', DIST / 'robots.txt')
    write(DIST / 'CNAME', 'coolbirbs.com\n')
    write(DIST / '.nojekyll', '')
    write(DIST / 'sitemap.xml', (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'<url><loc>{SITE}/</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>\n'
        '</urlset>\n'
    ))
    write(DIST / '404.html', '<!DOCTYPE html><meta charset="utf-8"><title>Not found</title>'
          '<script>location.replace("/");</script><a href="/">This bird does not exist.</a>\n')
    print(f'built {SEEDS + 1} pages into {DIST}')


if __name__ == '__main__':
    main()
