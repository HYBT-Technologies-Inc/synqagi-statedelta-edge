# Deploy into the existing GitHub repository

The archive is designed to be extracted into the root of the existing repository.

```bash
git clone https://github.com/HYBT-Technologies-Inc/synqagi-statedelta-edge.git
unzip -o synqagi-statedelta-edge-bootstrap-v0.1.0.zip -d synqagi-statedelta-edge
cd synqagi-statedelta-edge
python3 -m unittest discover -s tests -v
git add -A
git commit -m "feat: bootstrap SYNQAGI StateDelta Edge"
git push origin main
```

If the repository is already cloned locally:

```bash
cd synqagi-statedelta-edge
git pull --ff-only origin main
unzip -o ../synqagi-statedelta-edge-bootstrap-v0.1.0.zip -d .
python3 -m unittest discover -s tests -v
git add -A
git commit -m "feat: bootstrap SYNQAGI StateDelta Edge"
git push origin main
```

The commands overwrite the initial bootstrap documentation with the verified complete versions from this archive. They do not delete Git history.
