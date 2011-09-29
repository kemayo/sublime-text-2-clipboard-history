# Sublime Text 2 plugin: Clipboard History

Keep a history of your clipboard items. Let you paste them back in, as needed.

## Using

OSX: Press ctrl-alt-super-v to show the history.

Windows:  Press ctrl-alt-v to show the history.

## Limitations

The history will only contain items that were copied:

 * in Sublime Text
 * using ctrl-c or ctrl-x (*not* the menu items)

Anything that reloads the plugin will clear the saved history.

Pasting from the history may not play nicely with multiple selections.

## Installing

First, you need to have `git` installed and in your `$PATH`. Afterwards you may need to restart Sublime Text 2 before the plugin will work.

### OSX

    $ cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    $ git clone git://github.com/kemayo/sublime-text-2-clipboard-history.git ClipboardHistory

### Linux (Ubuntu like distros)

    $ cd ~/.config/sublime-text-2/Packages/
    $ git clone git://github.com/kemayo/sublime-text-2-clipboard-history.git ClipboardHistory

### Windows 7:

    Copy the directory to: "C:\Users\<username>\AppData\Roaming\Sublime Text 2\Packages"

### Windows XP:

    Copy the directory to: "C:\Documents and Settings\<username>\Application Data\Sublime Text 2\Packages"
