# `pure-ftpd` uploadscript with RC

- `pure-uploadscript`
  - [x] `pure-uploadscript` activated (2%)
  - [x] File name with `.exe` should be moved to `/home/ftp/hidden/.exe/` (4%)
  - [x] Record should be written in log file after violation file upload (3%)
- `ftp_watchd`
  - [x] `rc.d` auto start on boot (2%)
  - Service operation
    - [x] `pure-uploadscript` should be run in the background (2%)
    - [x] `start` / `status` / `stop` / `restart` (2%)
