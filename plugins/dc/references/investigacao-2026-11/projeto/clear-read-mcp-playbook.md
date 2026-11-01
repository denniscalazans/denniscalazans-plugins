# Clear Read the Web: MCP Playbook

CHECKED: 2026-10-08 · connectors-cleaned
SET_VERSION: 2026-10-14-r1

This file tells Claude which connector (MCP) to use for each job in this Project, what each one can do, and how to call it so the answer costs few tokens.
It extends section 4 of the Project instructions.
When this file and section 4 disagree, this file wins, because it is newer.

How this was checked:
- **Schema read on 7 and 8 de outubro de 2026** (parameters confirmed): Exa, Parallel Search, Valency (3 tools), Context7, alphaXiv (2 tools), PubMed (2 tools), ElevenLabs (the speech tools).
- **Connector list rechecked on 8 de outubro de 2026.** Jina Reader, Miro, Canva, Gamma, Spotify, bioRxiv and the second ElevenLabs connector are no longer in the tool list.
- **Known from the tool list only** (names and one-line descriptions): every other connector. Load the schema with `tool_search` before the first call, and never guess a parameter name.

## 1. Where the tokens go, and how to keep them

A connector costs tokens in three places.
Each place has its own saving rule.

| Cost | What causes it | Rule that saves it |
|---|---|---|
| The tool list | Every connected tool adds its name to every chat, even unused | Dennis switches off connectors this Project never uses (section 6). Done for most of them on 8 de outubro de 2026 |
| The schema | `tool_search` loads the full definition of each tool it returns | Search by the exact tool name, with `limit` 1 to 3. Load only what this article needs |
| The result | The text a call returns stays in the conversation until the end | Cap every call (section 1.1). This is the biggest cost by far |

### 1.1 The seven rules for cheap results

1. **Climb the ladder, and stop early.** Search snippet first. Then a targeted excerpt from one page. Then the full page. Only the source article itself always gets the full page.
2. **Cap every call.** Set the result count, the character limit, or the passage count on every call that has one. The defaults are sized for general use, so they are too big for a single fact-check.
3. **Ask the page a question.** When a tool accepts a question or an objective (Parallel `objective`, alphaXiv `queries`), use it. The tool then returns only the passages that answer, instead of the whole document.
4. **Batch.** Put several URLs or several queries in one call. One call with 5 URLs costs less than 5 calls.
5. **One engine per question.** Do not send the same question to web search, Exa and Parallel. Switch engines only when the first result is thin or off target.
6. **Reuse before you search.** Check the Biblioteca `facts` and `glossary` first. A stable fact checked in the last 6 months needs no new search.
7. **Keep big things on disk.** For a long PDF or dataset, download it in bash and search it with `grep` or `pdftotext`, so only the matching lines enter the conversation. For Biblioteca reads, use `out_dir` and open only the files needed.

### 1.2 What costs money or quota, not only tokens

| Connector | What is limited | Rule |
|---|---|---|
| ElevenLabs | Paid credits, about 1 credit per character | Estimate first. One generation. Never retry by calling again |
| Exa `agent_run` | Efforts `auto` and `ultra` are billed in dollars (default caps: 5 and 20 dollars) | Use `minimal` or `low` only. Never `auto` or `ultra` without Dennis's yes |
| Consensus | About 30 calls a month on the free plan | Only for a contested science claim, one call per article |
| Parallel Search | Free-tier rate limit per session | Create one `session_id` per conversation and reuse it on every call |

## 2. Routing: which tool for which job

| Job | First call | If it is not enough |
|---|---|---|
| Read the source article in full | Built-in `web_fetch` | Exa `web_fetch_exa` with a high `maxCharacters`, then Parallel `web_fetch` with `full_content: true` |
| Read a YouTube video | Exa `web_fetch_exa` on the video URL, with a high `maxCharacters` | "You tube transcriptor", then ask Dennis to paste |
| Check one claim, no URL known | Built-in `web_search` | Parallel `web_search` (2 or 3 queries in one call), or Exa `web_search_exa` with `numResults` 3 to 5 |
| Check one claim on a known page | Parallel `web_fetch` with an `objective` (returns excerpts only) | Exa `web_fetch_exa` with the default 3,000 characters |
| Find the study behind a claim | Valency `semantic_search_papers` (capped, section 3.3) | Consensus (contested science), PubMed (health) |
| Read an arXiv paper | alphaXiv `answer_pdf_queries`, all questions in one call | Built-in `web_fetch` on the arXiv page |
| Read another PDF | Built-in `web_fetch`, or download in bash and `grep` | Exa fetch, then Parallel fetch |
| Health or biomedical claim | PubMed `search_articles`, then `get_article_metadata` | Valency with `source: "pubmed"` |
| Library, framework or API fact | Context7 (2 calls) | Microsoft Learn for Microsoft and Azure; the official docs site |
| Recompute a number | bash, for plain arithmetic | Wolfram, for units, statistics and real-world data |
| Claim about an AI model or dataset | Hugging Face `hub_repo_details` | Web search |
| Claim about how people use AI at work | Anthropic Economic Index | Web search |
| What happened after the article | Built-in `web_search`. For a paper: Valency `get_citing_papers` with `sort_by: "year"` | Exa search |
| Many items to research at once (a list, a comparison table) | Exa `agent_run` with effort `low` and an `outputSchema` | Do the searches yourself |

### 2.1 When to use a connector, and when to leave it alone

Dennis decided on 7 de outubro de 2026: the connectors stay active, and Claude must judge each call.
A connector that sits unused costs almost nothing, because only its name is in the chat.
A call that was not needed costs a lot, because its result stays in the conversation.
So before each call, check the trigger.

| Connector | Use it when | Leave it alone when |
|---|---|---|
| Valency | The article cites a study, or makes a science claim that needs its source | The claim is news, opinion, or a fact that web search settles |
| PubMed | The claim is about health, medicine or biology | The topic is psychology outside medicine, economics, AI or any other field |
| Consensus | Scientists disagree on the claim | One good study or an official source already settles it |
| alphaXiv | The source or the cited study is an arXiv paper | The paper is on another site, or the abstract already answers |
| Parallel Search | A fact must be confirmed on a known page, or web search came back thin | Web search already answered the same question |
| Exa search | The ideal page is easier to describe than to keyword (a blog post, a comparison, a person) | Web search already answered the same question |
| Exa `agent_run` | The task is a list or table that needs many searches | The task is one question or one page |
| Context7, Microsoft Learn | The article states how a library, framework or API behaves | The claim is about a company, a product launch or an opinion |
| Wolfram | Units, statistics, or real-world data on a date | Plain arithmetic, which bash does for free |
| DeepL | The PT-BR translation of one term is uncertain | Any normal translation, which Claude does itself |
| Hugging Face | The article states facts about a model or dataset | The article only mentions AI in general |
| Anthropic Economic Index | The article is about how people use AI at work | Any other topic |
| Excalidraw | Dennis asks for a hand-drawn sketch in the chat | The diagram goes into the published guide |
| Notion, Calendar, Gmail | Dennis asks for that specific action | Every other case |

A simple test before any call: "Which sentence of the guide will this result support?"
If there is no such sentence, skip the call.

## 3. Core connectors, one by one

### 3.1 Exa (3 tools) · web search, page reader, research agent

- **`web_search_exa`**: search by meaning. `query` describes the ideal page ("blog post comparing X and Y"), not keywords. `objective` is required: say which facts to pull. `numResults` defaults to 10.
- **`web_fetch_exa`**: reads URLs as clean markdown. `urls` takes several at once. `maxCharacters` defaults to **3,000 per page**, which cuts a normal article.
- **`agent_run`**: a multi-step research agent that runs many searches and returns a structured result. It is long-running: it returns a `runId`, and you continue with that `runId`.

Smart use:
- Fact-check: `numResults` 3 to 5, and a precise `objective`. The highlights usually answer without a fetch.
- Source article or transcript: set `maxCharacters` high (about 40,000 for an article, more for a long video), or the text is cut.
- Verification of a side page: keep the 3,000 default.
- `agent_run`: only for list-shaped work, with a bounded `outputSchema`. Never start a second run for the same task. Check the first with `runId`.

### 3.2 Parallel Search (2 tools) · web search and focused extraction

- **`web_search`**: `objective` (one atomic goal) plus `search_queries` (2 or 3 keyword queries of 3 to 6 words). Its excerpts are usually enough to answer.
- **`web_fetch`**: up to 20 URLs. By default it returns only excerpts that match the `objective` (at most 200 characters). `full_content: true` returns the whole page, often tens of thousands of tokens.

Smart use:
- This is the cheapest way to confirm a claim on a known page: URL plus `objective`, default excerpt mode.
- Use `full_content: true` only for the source article.
- Reuse one `session_id` for the whole conversation.

### 3.3 Valency (38 tools) · academic papers across PubMed, arXiv, bioRxiv, medRxiv, PsyArXiv, SocArXiv

What it does: search by meaning, by title, abstract, author, venue or category. It also follows citations, finds similar papers, shows trends over time, and exports references.

The tools this Project needs:
- **`semantic_search_papers`**: natural-language query. Defaults: 20 results, abstracts included, 20 authors per paper.
- **`get_paper_by_id`**: one paper in full.
- **`get_citing_papers`**: who cited a paper. `sort_by: "year"` shows the newest follow-up work.
- **`find_similar_papers`**: related work from one seed paper.
- **`count_papers`** and **`get_keyword_trends`**: how much research exists, without returning the papers.

Smart use:
- Two steps. First a triage call: `limit: 5`, `include_abstract: false`, `max_authors: 3`. Then `get_paper_by_id` for the 1 or 2 papers that fit.
- Add `source` when the field is known (for example `"pubmed"`), because the query runs faster.
- Use `sort_by: "citations"` to find the reference study behind a popular claim.
- Valency schemas are the largest in this Project. Load one tool at a time by its exact name.

### 3.4 PubMed (7 tools) · biomedical literature

- `search_articles`, `get_article_metadata`, `find_related_articles`, `lookup_article_by_citation`, `convert_article_ids`, `get_full_text_article`, `get_copyright_status`.

Smart use:
- Search, then metadata (it has the abstract). That answers most fact-checks.
- `get_full_text_article` returns the whole paper, so call it only when the abstract does not settle the claim. It needs a PMC ID, which comes from the metadata or from `convert_article_ids`.
- Only for health and life sciences. Every use must cite PubMed and the article's DOI in the guide.

### 3.5 Consensus (1 tool) · what the research says overall

- `search`: ranked peer-reviewed papers for a question.
- Smart use: one call per article at most, only when a science claim is contested. Valency comes first for everything else.

### 3.6 alphaXiv (23 tools) · arXiv papers

- **`answer_pdf_queries`**: accepts an arXiv ID, a URL or a title. It returns only the most relevant pages, up to a fixed size.
- `get_paper_content`: the whole paper as text.
- `discover_papers`: ranked candidates for a topic.
- `read_files_from_github_repository`: reads a paper's code repository.
- The library, folder, feed and follow tools manage Dennis's alphaXiv account. This Project does not use them.

Smart use:
- Put every question about one paper in a single `answer_pdf_queries` call, one string per question. Extra questions are almost free, and a second call is not.
- A title is enough. There is no need to find the URL first.
- Use `get_paper_content` only when the paper itself is the source article of the guide.

### 3.7 Jina Reader · removed

Dennis removed this connector on 8 de outubro de 2026. It was answering "401 Unauthorized".
Its jobs moved: alphaXiv for arXiv papers, the built-in fetch or bash plus `grep` for other PDFs, and Parallel `web_fetch` with an `objective` to check a claim on a known page.
If he adds it again with an API key, its best feature is `read_url` with `question` and `topk`, which returns only the passages that answer.

### 3.8 Context7 (2 tools) · current docs for libraries and frameworks

- `resolve-library-id` (name to ID), then `query-docs` (ID plus one question).
- Smart use: one concept per query. At most 3 calls of each tool per question. Skip the resolve step when the ID is already known (format `/org/project`). Never put private code in a query.

### 3.9 Microsoft Learn (3 tools) · Microsoft and Azure docs

- `microsoft_docs_search` (short excerpts), `microsoft_docs_fetch` (a full page), `microsoft_code_sample_search`.
- Smart use: search first. Fetch only when the excerpt is cut.

### 3.10 Wolfram (3 tools) · numbers and computed facts

- `WolframAlpha` (natural-language question), `WolframLanguageEvaluator` (runs code), `WolframContext` (semantic lookup).
- Smart use: plain arithmetic goes to bash, which is free. Wolfram is for unit conversions, statistics, and real-world data such as population or exchange rates on a date.

### 3.11 ElevenLabs · audio

- The Project uses only the `creative_*` group: `creative_list_voices`, `creative_create_flow`, `creative_generate_speech`, `creative_get_flow_run_status`, and `creative_transcribe_audio`.
- The `agents_*` group (more than 100 tools) builds phone and chat agents. This Project never uses it.
- Only one ElevenLabs connector is active since 8 de outubro de 2026: the voice and speech one. It refuses image, video and music, which this Project does not need.
- Speech models offered: `eleven_v3`, `eleven_v4`, `eleven_multilingual_v2`, `eleven_turbo_v2_5`, `eleven_flash_v2_5`.
- Smart use: write the script with the `clear-listen` skill, then follow section 6.4 of the instructions and the project doc `claude/clear-read-audio-playbook.md`. Load each `creative_*` tool by its exact name, so the `agents_*` schemas never load.
- `creative_transcribe_audio` can turn a podcast file into a transcript when no transcript exists. It spends credits, so ask first.

### 3.12 Mermaid Chart (1 tool) and Excalidraw (2 tools) · diagrams

- Mermaid Chart `validate_and_render_mermaid_diagram`: checks the syntax of a diagram. The phone check script (`scripts/check_mermaid.cjs` of the clear-read skill, or the older `check_mermaid.js` in this Project) stays the real gate before publishing.
- Excalidraw `read_me` then `create_view`: a hand-drawn diagram in the chat. It does not go into the published page. Call `read_me` once per session, because it is long.

### 3.13 Google Drive (11 tools), Notion (47 tools), Google Calendar (9 tools), Gmail (30 tools)

- **Drive**: backup in the folder "Clear Read". Use `search_files` to find the folder, and `create_file` to save. Do not read back a file you just wrote. `update_file` changes only a file's title or folder, never its content, so a new version of a file is a new file (section 0 of the instructions: one subfolder per set).
- **Notion**: a mirror of the Biblioteca, only when Dennis asks. Search, then fetch one page. Create several pages in one `notion-create-pages` call.
- **Calendar**: review reminders, only after his yes for that action.
- **Gmail**: only on his explicit request. Prefer `create_draft` over `send_message`.

### 3.14 DeepL (9 tools), Hugging Face (3 tools), Anthropic Economic Index (9 tools), "You tube transcriptor" (1 tool)

- **DeepL**: `translate-text` for a term whose PT-BR translation is uncertain. Claude translates everything else itself.
- **Hugging Face**: `hub_repo_details` confirms facts about a model or dataset (license, release, size) when an article is about AI.
- **Anthropic Economic Index**: data on how people use Claude by country, occupation and task. Only for articles on that topic.
- **You tube transcriptor**: fallback only. It failed 3 times in testing.

## 4. Built-in tools that are not connectors

They cost no connector setup, so they come first when they fit.

- **Built-in `web_search` and `web_fetch`**: the default for research and for the source article. `web_fetch` accepts a token limit for the returned text.
- **bash with network access**: `curl` a public file to disk, then `grep` it. Good for long PDFs and CSV data.
- **Artifact tool**: publishes the guide and holds the Biblioteca database.
  - Read with `query` and a `where` filter instead of `list`, so only matching documents return.
  - Use `out_dir` to save documents as files instead of loading them into the conversation.
  - Write with `batch` (up to 50 writes). Change one phrase with `str_replace` instead of resending the document.
- **Inline visuals in the chat** (`show_widget`): for a quick diagram or interactive piece in the chat reply.
- **Image search**: photos in the chat, because the published page cannot load remote images.

## 5. Connected, but not for this Project

| Connector | What it does | Rule |
|---|---|---|
| Indeed (4 tools) | Job search | Never used here |
| Claude Docs | Editable documents | Guides are HTML pages, so use it only when Dennis asks for a document |
| Akelius, Atlassian, Microsoft 365 | Work systems | Connected to the account, but no tools appear in this Project's chats. Leave them off |

No longer in the tool list on 8 de outubro de 2026: Jina Reader, Miro, Canva, Gamma, Spotify, bioRxiv, and the second ElevenLabs connector.
Valency covers what bioRxiv did (`source: "biorxiv"` or `"medrxiv"`).

## 6. Setup actions for Dennis (they cut the cost of every chat)

1. **Done on 8 de outubro de 2026:** one ElevenLabs connector only, and Jina Reader, Miro, Canva, Gamma, Spotify and bioRxiv are out of this Project's chats.
2. **Still open:** switch off Indeed in this Project. It adds 4 tool names that are never used.
3. **Decided on 7 de outubro de 2026.** Valency, PubMed, Parallel Search, Wolfram, DeepL, alphaXiv, Excalidraw and Calendar stay active. This replaces the "switch off" list in the stack report of the same day. Section 2.1 says when to use each one and when to leave it alone.
