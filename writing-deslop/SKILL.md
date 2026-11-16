---
name: writing-deslop
description: Write or edit prose so it reads like a person wrote it, not a model. Strips AI tells (em-dash abuse, "It's not X, it's Y", "delve", stock fiction phrases, formulaic role-play replies) from blog posts, essays, articles, stories, role play, docs, and READMEs. Use when drafting any of these, or when asked to "deslop", "deslopify", "detrope", "remove AI tells", "humanize", or "make this sound less like AI". Accepts content inline or as a file path.
license: MIT
---

# Writing Deslop

Remove AI writing tropes from prose while preserving the author's meaning, facts, voice, and intent. The result should read like a person wrote it: varied, imperfect, specific.

## Step 0: identify the form

The tells differ by form, and so does what counts as a legitimate device. Decide which form you are working in before touching anything, then read the matching section of [references/forms.md](references/forms.md).

| Form | Examples | What changes |
|---|---|---|
| Expository | Blog post, essay, article, newsletter, README, docs, email | The general catalog applies as written. Blog posts have their own opener, closer, and SEO tells. |
| Fiction | Short story, novel chapter, scene, fan fiction, poem | Rhetorical devices are tools, not tells. Hunt stock phrases, named emotions, uniform character voices, tidy endings. Never change plot, POV, tense, or canon. |
| Role play | Collaborative fiction, character chat, tabletop narration, interactive story | Per-reply tells matter more than per-sentence ones: repeated reply shape, acting for the other player, drifting out of character. Keep the scene's established format. |

Mixed pieces (a blog post that opens with an anecdote, a story with an essayistic narrator) take the rules of whichever form each passage is in.

## Modes

- **Draft**: you are writing new content. Apply the catalog as you write, then do one rewrite pass over your own draft before returning it. Return the content only, with no change list.
- **Rewrite** (default for existing content): clean the content and return it, followed by a short change list.
- **Review** (asked to "review", "audit", "flag", or "what's wrong with this"): do not rewrite the piece and do not edit any file. Return `Findings:` as a numbered list of `"exact quote" → trope name → suggested fix`, then a one-line `Verdict:` on how tell-heavy it reads. One finding per instance; a trope that repeats many times gets one finding with a count and two example quotes.

When unsure between rewrite and review, rewrite.

## How to operate

1. **Get the content.** It may be pasted or a file path. Read the file if given one; search for it if the path is ambiguous. For role play, also read the character or persona definition and enough prior turns to know the established voice and format.
2. **Load the catalogs.** The general catalog is [references/tropes.md](references/tropes.md). The form-specific rules are in [references/forms.md](references/forms.md). Read both for any serious pass.
3. **Scan.** Flag every instance, counting repeats.
4. **Rewrite, don't just delete.** Replace each trope with plain, direct prose that does the same job. Keep voice, claims, and structure. Never invent facts, plot events, or character history to fill a gap.
5. **Apply edits.** Edit the file in place if you read from one. Otherwise produce the cleaned version.
6. **Return the result.** Full cleaned content, then (rewrite mode) a short plain list of what changed, such as "Removed 14 em dashes" or "Cut 6 stock physical reactions". In role play, return only the in-character reply unless asked for notes.

If another agent invoked you, your final message is the only thing it receives: it must contain the complete cleaned content, not a changelog alone.

## Guiding rule

Any single trope used once may be fine. The problem is repetition and clustering. Do not sand the writing into uniformity: one rhetorical question or one stray em dash is human. Cut the patterns, not the personality. In expository writing, when in doubt, favor the simplest plain phrasing. In fiction and role play, when in doubt, favor the concrete detail over the stock one, and the character's voice over a neutral one.

## Core tropes (short list)

The most common tells in any form. Full catalog: [references/tropes.md](references/tropes.md).

- **Word choice**: "delve", "utilize" (use), "leverage", "robust", "streamline", "harness"; magic adverbs ("quietly", "deeply", "fundamentally", "remarkably"); grandiose nouns ("tapestry", "landscape", "paradigm", "ecosystem"); "serves as" / "stands as" / "represents" where "is" works.
- **Sentence structure**: negative parallelism, the top tell ("It's not X, it's Y"); "Not X. Not Y. Just Z."; self-posed questions ("The X? A Y."); anaphora and rule-of-three abuse; filler transitions ("It's worth noting", "Importantly"); trailing "-ing" analyses ("…highlighting its importance"); false ranges ("from X to Y").
- **Paragraph structure**: short fragments as standalone paragraphs for manufactured emphasis; prose that is secretly a list.
- **Tone**: false suspense ("Here's the kicker"); "Think of it as…"; "Imagine a world where…"; "let's be honest"; stakes inflation; pedagogical voice ("Let's unpack"); vague attributions ("experts argue"); invented concept labels ("the X paradox").
- **Formatting**: em-dash addiction; bold-first bullets; decorative arrows and emoji.
- **Composition**: intro-then-recap at every level; one metaphor beaten ten times; the same thesis restated ten ways; "In conclusion"; acknowledge-then-dismiss closers.

Form-specific tells (short list; full rules in [references/forms.md](references/forms.md)):

- **Blog posts**: "In today's fast-paced world" openers; "Whether you're a beginner or an expert"; headline-as-colon-formula on every section; a closing call for comments; a summary that repeats the post.
- **Fiction**: stock physical reactions ("a breath she didn't know she was holding", "heart pounding in her chest"); emotions named instead of shown; every character speaking in the same composed, self-aware voice; conflict resolved the moment it appears; a reflective, hopeful last paragraph.
- **Role play**: the same reply shape every turn; ending every reply on a question to the other player; deciding the other player's actions or feelings; recapping what they just wrote; breaking character to comment or disclaim; the character softening into an agreeable version of itself.

## What you must not do

- Do not change the author's argument, conclusions, facts, plot, characters, point of view, or tense.
- Do not add new claims, sources, examples, events, or backstory.
- Do not flatten real voice into bland prose. A narrator or character who is pompous, florid, or repetitive on purpose stays that way.
- Do not over-correct: leave the occasional single trope if it works.
- Do not override an explicit house style, persona definition, or scene convention. If the caller says a trope is allowed here ("em dashes are fine", "this character speaks in triads", "keep the asterisk actions"), that wins over this catalog.
- Do not sanitize content. This skill edits style only; tone, darkness, and subject matter belong to the author.

### Things that are not proof of AI

Do not strip these on sight:

- An em dash used sparingly and well, including for interrupted dialogue.
- Curly quotes, clean grammar, correct spelling.
- Ordinary uses of "important", "significant", or "notable".
- A single rule of three, one rhetorical question, one metaphor.
- In fiction: sentence fragments, deliberate repetition, dialect, and long sentences. These are craft.

The test is density and clustering, never a single occurrence.

---

Derived from [deslopify](https://github.com/axel-pm/deslopify) by Axel Sooriah (MIT; see `LICENSE.txt`), whose catalog builds on [tropes.fyi](https://tropes.fyi) by Ossama Chahib. Source list: [references/sources.md](references/sources.md). The form-specific rules in `references/forms.md` are additions.
