package { 'nginx'
  ensure   -> present,
  provider -> '/usr/local/bin/apt',
}
