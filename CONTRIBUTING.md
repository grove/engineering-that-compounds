# Editing and publishing the collection

## Source and build

Each essay lives in `essays/` as Markdown. The opening heading is its title; an optional italic paragraph supplies its subtitle. `README.md` sets the reading order and the descriptions on the home page. Keep titles in both places identical.

The site generator uses Python's standard library. It supports headings, paragraphs, flat lists, blockquotes, fenced code blocks and inline links/emphasis/code. It deliberately has no package installation or JavaScript build step. The CSS follows the reader's light or dark preference; native audio works without JavaScript.

```sh
python3 site/build.py --check
python3 -m http.server --directory _site 8000
```

The check builds all pages and checks the reading order, essay titles, local links, page anchors and narration fingerprints. Audio is temporarily omitted from the generated site; the check still fails if an essay's audio no longer matches its text or the narration pipeline. Generated `_site/` files are not committed.

For an editorial preview before regenerating audio, `python3 site/build.py` builds without the narration freshness gate. Do not publish that preview until `--check` passes.

## Narration

The MP3s are generated locally with [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx). The default voice is `bf_emma` (British English), at speed `0.95`, matching the original collection. Audio is mono, 24 kHz, 64 kbps. MP3s remain committed under `site/audio/`, but are not currently copied into the published site.

Use Python 3.12 for the pinned narration dependencies:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r site/requirements-tts.txt
.venv/bin/python site/tts.py
```

The first run downloads the Kokoro v1.0 model and voice files into `.cache/kokoro/`. These model files and the virtual environment are ignored by Git. No speech-service account or API key is needed. Model and voice-file download URLs are defined in `site/tts.py`.

To regenerate one changed essay:

```sh
.venv/bin/python site/tts.py engineering-capital
```

To generate several essays concurrently, use `--workers 3 --threads 2`; reduce this on machines with less memory. `--model-dir PATH` uses an existing model cache. `--force` regenerates otherwise current files. Invalid essay slugs fail instead of silently doing nothing.

Narration reads the title, subtitle, headings and prose. Linked text is spoken without URLs; fenced code and any closing Sources, References or Further reading section are omitted. Long paragraphs are divided into bounded chunks, with pauses at section and paragraph boundaries.

Commit the changed Markdown, its MP3 and `site/audio/manifest.json` together. The manifest records source and audio checksums, engine, voice, speed and duration. Changes to the narration code invalidate the narration fingerprints so that a fresh build cannot silently mix two pipelines. Audio is written through temporary files and the manifest is saved after each completed essay, allowing an interrupted run to resume.

Before committing, run the build check and decode any changed audio:

```sh
python3 site/build.py --check
ffmpeg -v error -xerror -i site/audio/engineering-capital.mp3 -f null -
```

Listen to a sample, including any changed names or technical terms. Check the first and last paragraphs against the text. An MP3 decoding successfully says nothing about pronunciation.

## GitHub Pages

In the repository's **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source. This is a repository setting, not a file in the pull request. See [GitHub's publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

The workflow in `.github/workflows/pages.yml` validates pull requests and saves a `site-preview` artifact for review. Pull requests cannot deploy to the live site. After a merge to `main`, it publishes the checked `_site/` artifact to:

https://grove.github.io/engineering-that-compounds/

You can also run the workflow manually on `main`. The `github-pages` environment supplies the deployment URL. If that environment has an approval or branch rule, the repository administrator's rule still applies. Audio generation is separate from deployment; Pages serves the committed MP3s and does not need model downloads or a narration secret.

## Editorial approach

Use a specific engineering problem to carry an argument. Describe hypothetical examples as such. Link factual claims to primary sources, explain the limits of the evidence, and distinguish a proposed practice from an established result. Avoid invented quotations, personal anecdotes attributed to the author, and unqualified claims that AI saves time.

Each essay should add something the others need. Remove repeated slogans and summaries; give counterexamples enough space to affect the conclusion. A failed investment belongs in the collection as much as a successful one.

## Attribution

The generator and initial presentation/narration approach derive from [Software that improves with age](https://github.com/grove/software-that-improves-with-age), under Apache 2.0. Keep `LICENSE` and `NOTICE` with redistributed source. Kokoro ONNX and its model have their own upstream licenses; the model weights are not part of this repository.
