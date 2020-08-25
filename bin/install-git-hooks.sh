#!/usr/bin/env bash

REPO_DIR="$(git rev-parse --show-toplevel)"
PRE_COMMIT_SCRIPT="${REPO_DIR}/.git/hooks/pre-commit"
cat <<EOT > ${PRE_COMMIT_SCRIPT}
#!/usr/bin/env bash
set -xeEuo pipefail

for file in ${REPO_DIR}/git-hooks/*.sh ; do
     "\${file}"
done
EOT
chmod 0755 ${PRE_COMMIT_SCRIPT}
