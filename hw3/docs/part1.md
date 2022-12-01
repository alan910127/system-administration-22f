# Setup a file server with `pure-ftpd`

## Tasks

- [x] FTP over TLS (5%)

- Unix user `sysadm`

  - [x] Login from SSH (4%)
  - [x] Full access to `public` (3%)
  - [x] Full access to `upload` (4%)
  - [x] Full access to `hidden` (4%)

- Virtual user `ftp-vip1`, `ftp-vip2`

  - [x] Chrooted to `/home/ftp` (4%)
  - [x] Full access to `public` (4%)
  - [x] Full access to `hidden` (3%)
  - [x] Full access to `upload`, but can only delete their own files and directories (4%)

- Anonymous login

  - [x] Chrooted to `/home/ftp` (4%)
  - [x] Can only upload or download from `public` (3%)
  - [x] Can only upload or download from `upload` (4%)
  - [x] Can enter `/home/ftp/hidden` but cannot retrieve directory listing (4%)

## Configurations

```conf
# /usr/local/etc/pure-ftpd.conf

# Modify each setting, don't paste this file directly

# TLS only
TLS                          2

# chroot users except sysadm
ChrootEveryone               yes
TrustedGID                   21

# virtual users
PureDB                       /usr/local/etc/pureftpd.pdb

# anonymous users
AnonymousOnly                no
NoAnonymous                  no
AnonymousCanCreateDirs       no
AnonymousCantUpload          no
AntiWarez                    no
```

## System Setup

- Generate TLS key

  ```bash
  sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/pure-ftpd.pem -out /etc/ssl/private/pure-ftpd.pem
  ```

- Create `sysadm`

  ```bash
  sudo pw groupadd ftpadmin -g 21
  sudo pw useradd sysadm -g ftpadmin -c "FTP Admin" -d /home/ftp
  ```

- Create `ftp` (for anonymous login)

  ```bash
  sudo pw groupadd ftpanon
  sudo pw useradd ftp -g ftpanon -c "FTP Anonymous User" -d /home/ftp -s /sbin/nologin
  ```

- Create `ftpuser` (for virtual users to attach)

  ```bash
  sudo pw groupadd ftpuser
  sudo pw useradd ftpuser -g ftpuser -c "FTP Virtual User" -d /dev/null -s /sbin/nologin
  ```

- Create virtual users

  ```bash
  sudo pure-pw useradd ftp-vip1 -u ftpuser -d /home/ftp
  sudo pure-pw useradd ftp-vip2 -u ftpuser -d /home/ftp
  # Commit changes into PureDB
  sudo pure-pw mkdb
  ```

## Directories

### `/home/ftp`

- owner: `sysadm`
- group: `ftpuser`

### `public`

> - Everyone can download & upload file
> - Everyone can mkdir, rmdir, delete except anonymous

```bash
mkdir public
chmod 777 public
```

### `upload`

> - Everyone can upload & download
> - Everyone can mkdir except anonymous
> - Everyone can only delete & rmdir their own file or directory except anonymous and sysadm (sticky bit)

```bash
mkdir upload
chmod 1777 upload
```

### `hidden`

> - Create a directory called “treasure” inside hidden
> - Create a file called “secret” inside hidden/treasure
> - Anonymous can’t list /home/ftp/hidden (no `r`) but can enter hidden/treasure (has `x`) and show hidden/treasure/secret (has `r`)

```bash
mkdir -p hidden/treasure
chmod 771 hidden
```
