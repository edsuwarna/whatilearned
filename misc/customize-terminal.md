### Install ZSH

**macOS**

`brew install zsh`

**Ubuntu, Debian and derivatives**

`apt install zsh`

Verify installation by running  `zsh --verion`

Make zsh as deafult shell: `chsh -s $(which zsh)`

Test that it worked with `echo $SHELL`. Expected result: `/bin/zsh` or similar.

### Install oh-my-zsh

**Install oh-my-zsh via curl**

`sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`

**Install oh-my-zsh via wget**

`sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"`

Edit .zshrc file in your home directory to custom theme and add plugin.

oh-my-zsh themes: https://github.com/ohmyzsh/ohmyzsh/tree/master/themes

oh-my-zsh plugins: https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins
 