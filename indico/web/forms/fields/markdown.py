# This file is part of Indico.
# Copyright (C) 2002 - 2025 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

from wtforms import TextAreaField

from indico.util.i18n import _
from indico.web.forms.widgets import JinjaWidget


class IndicoMarkdownField(TextAreaField):
    """A Markdown-enhanced textarea.

    When using the editor you need to include the markdown JS/CSS
    bundles and also the MathJax JS bundle (even when using only
    the editor without Mathjax).

    :param editor: Whether to use the WMD widget with its live preview
    :param mathjax: Whether to use MathJax in the WMD live preview
    """

    widget = JinjaWidget('forms/markdown_widget.html', single_kwargs=True, rows=5)

    def __init__(self, *args, editor=False, mathjax=False, **kwargs):
        self.use_editor = editor
        self.use_mathjax = mathjax
        orig_id = kwargs['_prefix'] + kwargs['name']
        if self.use_editor:
            # WMD relies on this awful ID :/
            kwargs['id'] = 'wmd-input-f_' + orig_id
        else:
            kwargs.setdefault('description', _('You can use Markdown or basic HTML formatting tags.'))
        super().__init__(*args, **kwargs)
        self.orig_id = orig_id
