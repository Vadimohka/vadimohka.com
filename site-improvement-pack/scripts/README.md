# Pack scripts

Run from any directory:

```bash
python3 qa/site-improvement-pack/scripts/validate_pack.py
python3 qa/site-improvement-pack/scripts/next_task.py
python3 qa/site-improvement-pack/scripts/show_master_prompt.py
```

Optional online source check:

```bash
python3 qa/site-improvement-pack/scripts/check_source_links.py
```

The online checker is not part of the required offline QA because social platforms and publisher anti-bot rules can return false failures. Record inaccessible sources for manual review rather than silently deleting them.
