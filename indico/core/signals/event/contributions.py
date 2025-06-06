# This file is part of Indico.
# Copyright (C) 2002 - 2025 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

from indico.core.signals.event import _signals


contribution_created = _signals.signal('contribution-created', '''
Called when a new contribution is created. The `sender` is the new contribution.
If a contribution is cloned, the original one is passed in the `cloned_from` kwarg.
In this case, a `person_link_map` kwarg with the mapping between old and new
contribution person links is also passed.
''')

contribution_deleted = _signals.signal('contribution-deleted', '''
Called when a contribution is deleted. The *sender* is the contribution.
''')

contribution_updated = _signals.signal('contribution-updated', '''
Called when a contribution is modified. The *sender* is the contribution.
A dict containing ``old, new`` tuples for all changed values is passed
in the ``changes`` kwarg.
''')


subcontribution_created = _signals.signal('subcontribution-created', '''
Called when a new subcontribution is created. The `sender` is the new subcontribution.
If a subcontribution is cloned, the original one is passed in the `cloned_from` kwarg.
In this case, a `person_link_map` kwarg with the mapping between old and new
subcontribution person links is also passed.
''')

subcontribution_deleted = _signals.signal('subcontribution-deleted', '''
Called when a subcontribution is deleted. The *sender* is the subcontribution.
''')

subcontribution_updated = _signals.signal('subcontribution-updated', '''
Called when a subcontribution is modified. The *sender* is the subcontribution.
''')
