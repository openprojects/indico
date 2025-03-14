# This file is part of Indico.
# Copyright (C) 2002 - 2025 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from indico.core.db import db
from indico.core.db.sqlalchemy import PyIntEnum
from indico.core.db.sqlalchemy.searchable import fts_matches, make_fts_index
from indico.util.decorators import strict_classproperty
from indico.util.enum import RichIntEnum
from indico.util.string import MarkdownText, PlainText, RichMarkup


class RenderMode(RichIntEnum):
    """Rendering formats that a description can be written in."""

    __titles__ = [None, 'HTML', 'Markdown', 'Plain Text']
    html = 1
    markdown = 2
    plain_text = 3


RENDER_MODE_WRAPPER_MAP = {
    RenderMode.html: RichMarkup,
    RenderMode.markdown: MarkdownText,
    RenderMode.plain_text: PlainText
}


class RenderModeMixin:
    """Mixin to add a plaintext/html/markdown-enabled column."""

    possible_render_modes = {RenderMode.plain_text}
    default_render_mode = RenderMode.plain_text

    @declared_attr
    def render_mode(cls):
        # Only add the column if there's a choice
        # between several alternatives
        if len(cls.possible_render_modes) > 1:
            return db.Column(
                PyIntEnum(RenderMode),
                default=cls.default_render_mode,
                nullable=False
            )
        else:
            return cls.default_render_mode

    @classmethod
    def _render_getter(cls, attr_name):
        def _getter(self):
            selected_mode = (self.default_render_mode
                             if len(self.possible_render_modes) == 1 or self.render_mode is None
                             else self.render_mode)
            description_wrapper = RENDER_MODE_WRAPPER_MAP[selected_mode]
            return description_wrapper(getattr(self, attr_name))
        return _getter

    @classmethod
    def _render_setter(cls, attr_name):
        def _setter(self, value):
            setattr(self, attr_name, value)
        return _setter

    @classmethod
    def _render_expression(cls, attr_name):
        def _expression(cls):
            return getattr(cls, attr_name)
        return _expression

    @classmethod
    def create_hybrid_property(cls, attr_name):
        """Create a hybrid property that does the rendering of the column.

        :param attr_name: a name for the attribute the unprocessed value can be
                          accessed through (e.g. `_description`).
        """
        return hybrid_property(cls._render_getter(attr_name), fset=cls._render_setter(attr_name),
                               expr=cls._render_expression(attr_name))


class DescriptionMixin(RenderModeMixin):
    marshmallow_aliases = {'_description': 'description'}

    @declared_attr
    def _description(cls):
        return db.Column(
            'description',
            db.Text,
            nullable=False,
            default=''
        )

    description = RenderModeMixin.create_hybrid_property('_description')


class SearchableDescriptionMixin(DescriptionMixin):
    @strict_classproperty
    @classmethod
    def __auto_table_args(cls):
        return (make_fts_index(cls, '_description', 'description'),)

    @classmethod
    def description_matches(cls, search_string, exact=False):
        """Check whether the description matches a search string.

        To be used in a SQLAlchemy `filter` call.

        :param search_string: A string to search for
        :param exact: Whether to search for the exact string
        """
        return fts_matches(cls.description, search_string, exact=exact)
