# Dépôt de test pour les hook git

## Créer les dépôts pour tester

Executer soit init_dir_for_test.py soitinit_dir_for_test.sh

## Structure du dépot après initialisation

Le repertoire `client` contient un dépôt git normal avec comme remote origin
qui pointe sur le répertoir `server` qui lui même est un dépot git bare.

Le repertoire `hook-py` contient des hooks de test écrits en python

## Ajout d'un hook post-receive

```bash
cp "hook-py/post-receive" "server/.git"
```

Tester si le script fonction

```bash
echo 'test' >> 'client/test' && git -C './client' add . && git -C './client' commit -m "test" -m "body" && git -C './client' push origin
```

## Installation pour un deploiement auto

### Sur le serveur

Créer un dépot git `bare` sur le serveur et mettre le hook post-receive.

```bash
git init --bare ~/project.git
curl -L -o ~/project.git/hooks/post-receive https://raw.githubusercontent.com/marc31/git_hook/main/hook-py/post-receive
chmod +x project.git/hooks/post-receive
```

Il faut modifier les variables dans post-receive :

```python
# Le chemin où les fichiers doivent être déployer sur le serveur
targetDir="../target"      
# Le chemin du dépôt bare
gitBareDir="../server"
# Les branches qui doivent initialiser un déploiement
branchToDeploy=["prod"]
```

Maintenant sur la machine de dev lorsque l'on veut lancer un déploiement

```bash
# Mettre le répertoire courant qui contient ce que l'on veut déployer
cd monrep
# Rajouter un `remote` vers le dépôt bare
git remote add deploy USER@SERVER_BARE_URL:PATH_DU_DEPOT_BARE
```

Quand on veut deployer il suffit maintenant de faire sur la machine de dev

```bash
git push deploy
```
