---
layout: post
title: Sample Post
author: John Doe
website: https://github.com/user_name/repo_name
img: posts/sample-post.png
tags: [TUI, Terminal, Linux]
description: This is the description, used for both the front page summary and the SEO
hidden: true
---

## This is a hidden file for testing styling

## Example Python

```py
class SpinnerWidget(Static):
    def __init__(self, spinner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._spinner = Spinner(spinner)  

    def on_mount(self) -> None:
        self.update_render = self.set_interval(1 / 60, self.update_spinner)

    def update_spinner(self) -> None:
        self.update(self._spinner)
```

## Example Markdown Table

| Header 1     | Header 2     | Header 3     |
|--------------|--------------|--------------|
| Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 |
| Row 2, Col 1 | Row 2, Col 2 | Row 2, Col 3 |
| Row 3, Col 1 | Row 3, Col 2 | Row 3, Col 3 |

## GITHUB

[{{ page.website }}]({{ page.website }})
