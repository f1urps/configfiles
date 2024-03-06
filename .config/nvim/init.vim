source /usr/share/vim/vim90/defaults.vim

set number
set expandtab
set tabstop=4
set softtabstop=4
set shiftwidth=4
set laststatus=2

nnoremap cs c/"<CR>
nnoremap <CR> :noh<CR><CR>

" Disable error highlighting of Sway config files
" https://github.com/vim/vim/issues/10231
highlight link i3ConfigError Normal

