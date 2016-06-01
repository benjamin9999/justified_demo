import urwid
from pydux.create_store import create_store
from urwid_pydux import subscribe_urwid_redraw

from .components import App
from .reducers import root_reducer
from .actions import *
from justified import MOBY


def main():
    store = create_store(root_reducer)
    root = App(store=store)

    def keyhandler(key):
        dispatch = store['dispatch']
        state = store['get_state']()
        if key in ('=', '+'):
            dispatch(grow_text_width())
            return True
        if key == '-':
            dispatch(shrink_text_width())
            return True
        if key == 'f':
            dispatch(toggle_frame())
            return True
        if key == 'i':
            dispatch(toggle_edit())
            return True
        if key == 'm':
            dispatch(toggle_method())
            return True
        if key == 'c':
            dispatch(update_text('', 'user'))
            return True
        if key == 's':
            dispatch(update_text(MOBY, 'user'))
            return True
        if key == 'esc':
            if state['show_editor']:
                dispatch(toggle_edit())
            else:
                dispatch(quit_app())
            return True

    loop = urwid.MainLoop(root, unhandled_input=keyhandler)
    subscribe_urwid_redraw(store, loop)

    def maybe_quit():
        if store['get_state']()['should_quit']:
            raise urwid.ExitMainLoop()

    store['subscribe'](maybe_quit)

    loop.run()


if __name__ == '__main__':
    main()
