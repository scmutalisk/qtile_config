# base
import os
import subprocess

# qtile
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger

# 3rd parties
from psutil import sensors_temperatures

mod = "mod4"
my_terminal = "kitty"
home_path = os.path.expanduser('~')
keys = [
    # Switch to next layout
    Key([mod], "space", lazy.layout.next()),
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Volume
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),

    # Spawn programs
    Key([mod], "Return", lazy.spawn("dmenu_run -h 24 -p 'Run: '")),
    Key([mod, "shift"], "Return", lazy.spawn(my_terminal)),
    Key([mod, "shift"], "e", lazy.spawn('emacsclient -nc')),
    Key([mod, "shift"], "f", lazy.spawn('firefox')),
    Key([mod, "shift"], "q", lazy.spawn('qutebrowser')),
    Key([mod, "shift"], "m", lazy.spawn('thunar')),

    # Toggle between different layouts
    Key([mod], "Tab", lazy.next_layout()),

    # Kill current window
    Key([mod, "shift"], "c", lazy.window.kill()),

    # Restart QTile
    Key([mod, "control"], "r", lazy.restart()),

    # Logout/Leave Session
    Key([mod, "control"], "q", lazy.shutdown()),
]

# Custom group names
group_names = ("www", "dev", "chat", "mus", "vid", "etc")

# Generate groups
groups = [Group(name=i, layout="monadtall") for i in group_names]

# Switch or move focused window to group
for key, i in enumerate(group_names, 1):
    keys.extend([
        Key([mod], str(key), lazy.group[i].toscreen()),
        Key([mod, 'shift'], str(key), lazy.window.togroup(i))
    ])

layout_theme = {
    "border_width": 2,
    "margin": 16,
    "border_focus": "#c8a7c7",
    "border_normal": "#1D2330"
}

layouts = [
    layout.MonadTall(**layout_theme, name='monadtall'),
    layout.Max(**layout_theme, name='max'),
]

colors = [
    "#292d3e",
    "#434758",
    "#ffffff",
    "#ff5555",
    "#8d62a9",
    "#668bd7",
    "#e1acff"
]

widget_defaults = {
    'font': 'Hack',
    'fontsize': 10,
    'padding': 6
}

extension_defaults = widget_defaults.copy()

custom_sep_widget = widget.Sep(
    padding=14,
    linewidth=1,
    background=colors[0],
    foreground=colors[1]
)

screens = [
    Screen(
        top=bar.Bar([
            widget.GroupBox(
                font="Hack Bold",
                margin=4,
                padding=4,
                borderwidth=3,
                active=colors[2],
                inactive=colors[2],
                rounded=False,
                highlight_color=colors[1],
                highlight_method="line",
                this_current_screen_border=colors[3],
                this_screen_border=colors[4],
                other_current_screen_border=colors[0],
                other_screen_border=colors[0],
                foreground=colors[2],
                background=colors[0]
            ),
            custom_sep_widget,
            widget.WindowName(
                font='Hack',
                fontsize=12,
                foreground=colors[6],
                background=colors[0],
                padding=None
            ),
            custom_sep_widget,
            widget.Systray(
                background=colors[0],
                padding=6,
            ),
            custom_sep_widget,
            widget.GenPollText(
                font="Hack Bold",
                padding=0,
                update_interval=1,
                foreground="#00ff00",
                background=colors[0],
                func=lambda: "CPU: {0}℃".format(str(int(sensors_temperatures()['acpitz'][0].current)) or "None")
            ),
            custom_sep_widget,
            widget.Memory(
                background=colors[0],
                foreground="#ffff66",
                padding=0,
                font="Hack Bold",
                format="Memory: {MemUsed}M/{MemTotal}M",
                update_interval=1
            ),
            custom_sep_widget,
            widget.DF(
                partition="/home",
                format="/home: {uf}{m}",
                padding=0,
                font="Hack Bold",
                background=colors[0],
                foreground="#00ffff",
                visible_on_warn=False
            ),
            custom_sep_widget,
            widget.Clock(
                background=colors[0],
                foreground="#f7347a",
                format="%r",
                font="Hack Bold",
                padding=0
            ),
            custom_sep_widget,
            widget.CurrentLayoutIcon(
                background=colors[0],
                padding=0,
                scale=0.7
            ),
            custom_sep_widget
        ], size=24),
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(title='branchdialog'),
    Match(title='pinentry'),
])
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def startup():
    subprocess.call([home_path + '/.config/qtile/autostart.sh'])

# @hook.subscribe.client_new
# def func(c):
#     logger.debug(c.name)

# @hook.subscribe.addgroup
# def func(name):
#     logger.debug(name)

# @hook.subscribe.changegroup
# def func():
#     logger.debug("group changed")
