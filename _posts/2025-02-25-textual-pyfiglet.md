---
layout: post
title: textual-pyfiglet
author: Edward Jazzhands
url: https://github.com/edward-jazzhands/textual-pyfiglet
img: posts/textual-pyfiglet.png
tags: [BigText, ASCII]
# description is only for metadata / SEO
description: A library that makes it easy to integrate PyFiglet into Textual. It adds a 'FigletWidget' that handles all the hard stuff for you.
---

Textual-PyFiglet is an implementation of [PyFiglet](https://github.com/pwaller/pyfiglet) for Textual.

It provides a `FigletWidget` class which handles all the hard stuff for you. Any text generated will automatically crop to the container that it's inside of - so you can just set the size of the FigletWidget where you need, and it'll handle the alignment and cropping automatically.

It can also write or update in real time - It can be tied to an Input or TextArea widget, or have text fed into it programmatically.

See the Github page for installation and to give it a star if you find it useful.

## GITHUB

[{{ page.url }}]({{ page.url }})

## DEMO

![Demo GIF](https://raw.githubusercontent.com/edward-jazzhands/textual-pyfiglet/refs/heads/main/demo.gif)
