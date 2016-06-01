from __future__ import absolute_import

from urwid import (
    connect_signal,
    Overlay, Frame, SolidFill,
    LineBox, Text, Filler, Padding, GridFlow, Edit,
    MIDDLE, CENTER, LEFT, RIGHT, TOP, BOTTOM, RELATIVE, CLIP,
)
from urwid_pydux import ConnectedComponent, Component

from justified import KnuthPlassFormatter, GreedyFormatter
from .constants import KNUTH
from .actions import update_text, toggle_edit


class App(ConnectedComponent):
    def map_state_to_props(self, state, own_props):
        if state['method'] == KNUTH:
            desc = 'Knuth-Plass'
        else:
            desc = 'Greedy'

        return {
            'width': state['width'],
            'frame': state['frame'],
            'method_description': desc,
            'method': state['method'],
            'text': state['text'],
            'show_editor': state['show_editor'],
        }

    def component_will_mount(self, props):
        self.editor = Filler(
            SampleEditor(store=props['store']),
            valign=TOP
        )

    def render_component(self, props):
        overlay_width = props['width']

        content = WrappedTextBox(
            text=props['text'],
            width=overlay_width,
            type=props['method'],
        )

        if props['frame']:
            content = LineBox(Padding(
                content, left=4, right=4,
            ))
            overlay_width += 2 + 4 + 4
            height_pct = 60
        else:
            height_pct = 100

        help_text = ('<-> & <+> width, '
                     '<C> clear, '
                     '<S> sample, '
                     '<F> frame, '
                     '<M> method, '
                     '<I> editor, '
                     '<Esc> quit')

        content = Frame(
            body=content,
            header=GridFlow(cells=[
                Text('Width: {}'.format(props['width'])),
                Text('Method: {}'.format(props['method_description'])),
            ], cell_width=20, h_sep=0, v_sep=0, align=LEFT)
        )

        content_on_filler = Overlay(
            top_w=content,
            bottom_w=SolidFill(' '),
            align=CENTER if props['frame'] else LEFT,
            width=overlay_width,
            valign=MIDDLE if props['frame'] else TOP,
            height=(RELATIVE, height_pct),
            min_width=20,
            min_height=20,
        )

        help_on_content_on_filler = Overlay(
            top_w=Filler(Text(help_text, align=RIGHT), bottom=1),
            bottom_w=content_on_filler,
            align=RIGHT,
            width=len(help_text),
            valign=BOTTOM,
            height=1,
        )

        if props['show_editor']:
            return Overlay(
                top_w=Frame(
                    body=LineBox(self.editor),
                    footer=Text('<Esc> to close editor')
                ),
                bottom_w=content_on_filler,
                align=RIGHT,
                valign=MIDDLE,
                height=(RELATIVE, 100),
                width=40,
            )
        else:
            return help_on_content_on_filler


class SampleEditor(ConnectedComponent):
    def map_state_to_props(self, state, own_props):
        # because urwid sends signals _before_ updating
        # the edit_text, we need to avoid a feedback loop
        # if the last edit was by the editor, don't update
        return {
            'text': state['text'],
            'rebuild_editor': state['last_edit_by'] == 'user',
        }

    def map_dispatch_to_props(self, dispatch, own_props):
        def on_change(new_text):
            dispatch(update_text(new_text, 'editor'))

        def on_exit():
            dispatch(toggle_edit())
        return {
            'on_change': on_change,
            'on_exit': on_exit,
        }

    def component_will_mount(self, props):
        self.editor = self.make_editor(props)

    def make_editor(self, props):
        return LiveEdit(edit_text=props['text'],
                        multiline=True,
                        on_change=props['on_change'],
                        on_escape=props['on_exit'])

    def render_component(self, props):
        if props['rebuild_editor']:
            self.editor = self.make_editor(props)
        return self.editor


class LiveEdit(Component):
    """edit box with change and exit callbacks"""
    prop_types = {
        'edit_text': int,
        'multiline': int,
        'on_change': int,
        'on_escape': int,
    }

    def component_will_mount(self, props):
        self.edit = EscapableEdit(caption='',
                                  edit_text=props['edit_text'],
                                  multiline=props['multiline'],
                                  on_escape=props['on_escape'])

        def on_change(edit, new_text):
            # warning, edit.edit_text != new_text yet!!
            props['on_change'](new_text)

        connect_signal(self.edit, 'change', on_change)

    def render_component(self, props):
        return self.edit


class EscapableEdit(Edit):
    """subclass of urwid Edit that calls a handler if escape is pressed"""
    def __init__(self, caption='', edit_text='',
                 multiline=False, on_escape=None):
        super(EscapableEdit, self).__init__(caption=caption,
                                            edit_text=edit_text,
                                            multiline=multiline)
        self.on_escape = on_escape

    def keypress(self, size, key):
        if self.on_escape and key == 'esc':
            self.on_escape()
            return True
        return super(EscapableEdit, self).keypress(size, key)


class WrappedTextBox(Component):
    """justified text box"""
    prop_types = {
        'text': int,
        'width': int,
        'type': int,
    }

    def render_component(self, props):
        if props['type'] == KNUTH:
            formatter = KnuthPlassFormatter
        else:
            formatter = GreedyFormatter
        wrapped = formatter(props['width']).format(props['text'])
        return Padding(
            PreformattedTextBox(text=wrapped, valign=TOP),
            width=props['width'],
        )


class PreformattedTextBox(Component):
    """boxed text object with wrap disabled"""
    prop_types = {
        'text': int,
        'valign': int,
    }

    def render_component(self, props):
        return Filler(Text(props['text'], wrap=CLIP), valign=props['valign'])
