### Install ZSH

**macOS**

`brew install zsh`

**Ubuntu, Debian dan turunannya**

`apt install zsh`

Verifikasi instalasi dengan menjalankan `zsh --version`

Jadikan zsh sebagai shell default: `chsh -s $(which zsh)`

Tes dengan `echo $SHELL`. Hasil yang diharapkan: `/bin/zsh` atau sejenisnya.

### Install oh-my-zsh

**Install oh-my-zsh via curl**

`sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`

**Install oh-my-zsh via wget**

`sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"`

Edit file .zshrc di home directory untuk mengganti tema dan menambahkan plugin.

Tema oh-my-zsh: https://github.com/ohmyzsh/ohmyzsh/tree/master/themes

Plugin oh-my-zsh: https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins
