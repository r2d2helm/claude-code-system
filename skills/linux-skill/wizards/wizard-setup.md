# Wizard: Server Hardening Initial

Assistant de securisation initiale d'un serveur Linux.

## Questions

1. **Distribution** : Ubuntu, Debian, RHEL/Rocky
2. **Role** : Web server, App server, Database, Docker host, General
3. **SSH** : Port custom ? Cle SSH deja copiee ?
4. **Firewall** : Ports a ouvrir (22, 80, 443, custom)
5. **Utilisateur** : Creer un utilisateur deploy ?

## Etapes

### 1. Mise a jour systeme

```bash
sudo apt update && sudo apt upgrade -y    # Debian/Ubuntu
sudo dnf update -y                         # RHEL/Rocky
```

### 2. Creer utilisateur non-root

```bash
sudo adduser deploy
sudo usermod -aG sudo deploy
sudo mkdir -p /home/deploy/.ssh
sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys
```

### 3. Securiser SSH

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo tee -a /etc/ssh/sshd_config.d/hardening.conf << 'EOF'
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowUsers deploy
EOF
sudo systemctl restart sshd
```

### 4. Firewall

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 5. fail2ban

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 6. Mises a jour automatiques

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Verification

```bash
# Tester SSH avec le nouvel utilisateur AVANT de fermer la session root
ssh deploy@<server> -p <port>
```
