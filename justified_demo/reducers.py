from pydux.extend import extend

from .constants import *
from justified import MOBY


def root_reducer(state=None, action=None):
    if state is None:
        state = {
            'text': MOBY,
            'width': 60,
            'frame': True,
            'center': True,
            'method': KNUTH,
            'should_quit': False,
            'show_editor': False,
            'last_edit_by': None,
        }

    if action['type'] == GROW_TEXT_WIDTH:
        return extend(state, {'width': min(state['width'] + 1, 256)})
    if action['type'] == SHRINK_TEXT_WIDTH:
        return extend(state, {'width': max(state['width'] - 1, 20)})
    if action['type'] == TOGGLE_FRAME:
        return extend(state, {'frame': not state['frame']})
    if action['type'] == TOGGLE_EDIT:
        return extend(state, {'show_editor': not state['show_editor']})
    if action['type'] == TOGGLE_METHOD:
        return extend(
            state,
            {'method': GREEDY if state['method'] == KNUTH else KNUTH}
        )
    if action['type'] == UPDATE_TEXT:
        return extend(
            state,
            {'text': action['text']},
            {'last_edit_by': action['who']},
        )
    if action['type'] == QUIT_APP:
        return extend(state, {'should_quit': True})
    return state
