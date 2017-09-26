# Steep
Steep is the **Sublime TTS External Editor Plugin**. Its a [Sublime Text](https://www.sublimetext.com/) plugin for editing scripts in [Tabletop Simulator](http://berserk-games.com/tabletop-simulator/). The plugin allows easy modification, testing, and execution of Tabletop Simulator's Lua scripts. This is the Sublime Text counterpart to the provided [Atom Editor Plugin](http://berserk-games.com/knowledgebase/atom-editor-plugin/).

## Installation
The plugin is unfinished and currently there is no installer. You may still install the plugin to test, use, or develop it in its current state.

To build the plugin yourself you may package the plugin as a directory in the `Packages` resource directory. Alternatively, you may create a zip compressed file with the extension `.sublime-package` and place it in the `Installed Packages` resource directory. To simplify this you may `git clone` into `Packages`.

Sublime Text recources location:
- Windows: `%APPDATA%\Sublime Text 3`
- Linux: `~/.config/sublime-text-3`
- Mac `~/Library/Application Support/Sublime Text 3`

[Package Control](https://packagecontrol.io/) support will come soon.

## Developing
To develop the plugin its best to install it in `Packages` using `git clone` (see [Installation](#installation)). Once installed in this way Sublime Text will automatically reload the plugin when changes to the plugin are made.

## Issues
Submit any issues or bugs through the GitHub issue tracker.

## Contributing
If you wish to contribute please read [CONTRIBUTING.md](CONTRIBUTING.md) for contributing guidelines and the process for submitting a pull request.

## Authors
- Lucas Gangstad - [LastTalon](https://github.com/LastTalon)

See also the [contributors](https://github.com/LastTalon/Steep/contributors).

## License
Steep is licensed under the zlib License. See [LICENSE.md](LICENSE.md) for details.
