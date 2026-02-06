# Commande: /lx-users

Gestion des utilisateurs et groupes.

## Syntaxe

```
/lx-users [action] [username]
```

## Actions

```bash
# Lister les utilisateurs (humains)
awk -F: '$3 >= 1000 && $3 < 65534 {print $1, $3, $6, $7}' /etc/passwd

# Ajouter un utilisateur
sudo adduser <username>
sudo usermod -aG sudo <username>   # Ajouter au groupe sudo

# Supprimer un utilisateur
sudo deluser --remove-home <username>

# Modifier
sudo usermod -l <newname> <oldname>    # Renommer
sudo usermod -aG <group> <username>    # Ajouter au groupe
sudo chsh -s /bin/bash <username>      # Changer shell

# Groupes
groups <username>
sudo groupadd <group>
sudo groupdel <group>

# Connexions recentes
last -n 20

# Utilisateurs connectes
who
w

# Configurer cle SSH
sudo -u <username> mkdir -p ~/.ssh
sudo -u <username> chmod 700 ~/.ssh
# Ajouter la cle dans ~/.ssh/authorized_keys
```

## Exemples

```bash
/lx-users list                 # Lister les utilisateurs
/lx-users add deploy           # Creer utilisateur deploy
/lx-users sudo deploy          # Ajouter aux sudoers
/lx-users connected            # Qui est connecte
```
