#!/usr/bin/env bash
set -euo pipefail

STEP=0
fail() { echo "[${STEP}/15] failed: $*" >&2; exit 1; }
run_step() { STEP="$1"; shift; echo "[${STEP}/15] $*"; }

run_step 1 "checking platform and target"
. /etc/os-release
[ "${VERSION_ID:-}" = "24.04" ] || fail "Ubuntu 24.04 is required"
[ ! -e /opt/aios ] || fail "/opt/aios already exists; choose a fresh box"
[ -z "${ANTHROPIC_API_KEY:-}" ] || fail "ANTHROPIC_API_KEY is forbidden; use Claude subscription or Bedrock auth"

run_step 2 "installing system packages"
# Existing Jarvis boxes may have an old GitHub CLI apt source whose signing key
# has expired. It is not needed by AIOS; keep a reversible copy out of apt's
# active sources so the required Ubuntu/Node repositories can update normally.
for source in /etc/apt/sources.list.d/*.list; do
  [ -f "$source" ] || continue
  if grep -q "cli.github.com" "$source"; then
    mv "$source" "$source.aios-disabled"
  fi
done
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-venv git ffmpeg curl ca-certificates lsb-release

run_step 3 "installing Node 22 and Claude Code prerequisites"
node_major="$(node --version 2>/dev/null | sed 's/^v//' | cut -d. -f1 || true)"
if [ -z "$node_major" ] || [ "$node_major" -lt 22 ]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs
fi
node_major="$(node --version | sed 's/^v//' | cut -d. -f1)"
[ "$node_major" -ge 22 ] || fail "Node 22 or newer is required (found $(node --version))"
command -v npm >/dev/null || fail "npm is required for Claude Code"

run_step 4 "installing Claude Code"
npm install -g @anthropic-ai/claude-code

run_step 5 "creating the aios user and private folders"
id aios >/dev/null 2>&1 || useradd --system --create-home --home-dir /opt/aios --shell /usr/sbin/nologin aios
install -d -o aios -g aios -m 700 /opt/aios /opt/aios/vault /opt/aios/vault/documents /opt/aios/vault/context /opt/aios/var

run_step 6 "cloning the application"
git clone --branch "${AIOS_BRANCH:-main}" --single-branch "${AIOS_REPO:-https://github.com/Govenor001/the-blueprint-aios.git}" /opt/aios/app
chown -R aios:aios /opt/aios

run_step 7 "creating the Python environment"
sudo -u aios python3 -m venv /opt/aios/venv
sudo -u aios /opt/aios/venv/bin/pip install -r /opt/aios/app/requirements.txt -r /opt/aios/app/dashboard/requirements.txt

run_step 8 "creating the environment file"
[ -n "${DASHBOARD_PASSWORD:-}" ] || fail "set DASHBOARD_PASSWORD to a strong value before installation"
if [ ! -e /opt/aios/.env ]; then
  install -o aios -g aios -m 600 /dev/null /opt/aios/.env
  printf 'DASHBOARD_PASSWORD=%s\n' "$DASHBOARD_PASSWORD" > /opt/aios/.env
fi
echo "Dashboard password saved in /opt/aios/.env; optional connectors can be added there later."

selected_route="${AIOS_MODEL_ROUTE:-claude-subscription}"
case "$selected_route" in
  claude-subscription|bedrock|openrouter) ;;
  *) fail "AIOS_MODEL_ROUTE must be claude-subscription, bedrock, or openrouter" ;;
esac
install -o aios -g aios -m 600 /dev/null /opt/aios/route.env
printf 'AIOS_MODEL_ROUTE=%s\n' "$selected_route" > /opt/aios/route.env
if [ "$selected_route" = "bedrock" ]; then
  printf 'CLAUDE_CODE_USE_BEDROCK=1\nAWS_REGION=%s\n' "${AWS_REGION:-us-east-1}" >> /opt/aios/route.env
fi

run_step 9 "Claude subscription authentication"
if [ "$selected_route" = "bedrock" ]; then
  echo "Bedrock route selected; Claude subscription setup-token is not required."
else
  echo "A browser link will open. Approve it on your phone, then paste the code back."
  sudo -u aios claude setup-token
  verification="$(sudo -u aios claude -p 'say ok' 2>/dev/null || true)"
  printf '%s\n' "$verification" | grep -qiE '(^|[^a-z])ok([^a-z]|$)' || fail "Claude authentication did not verify; rerun sudo -u aios claude setup-token"
fi

run_step 10 "optional local model"
echo "Tier 1 is optional; vault search falls back to keyword matching if it is unavailable."

run_step 11 "installing systemd services and schedules"
install -o root -g root -m 644 /opt/aios/app/deploy/systemd/aios-dashboard.service /etc/systemd/system/aios-dashboard.service
install -o root -g root -m 644 /opt/aios/app/deploy/systemd/aios-bridge.service /etc/systemd/system/aios-bridge.service
for unit in /opt/aios/app/deploy/timers/*; do
  install -o root -g root -m 644 "$unit" "/etc/systemd/system/$(basename "$unit")"
done
systemctl daemon-reload

run_step 12 "keeping the dashboard private"
if [ -n "${AIOS_DOMAIN:-}" ]; then
  case "$AIOS_DOMAIN" in
    *[!a-zA-Z0-9.-]*) fail "AIOS_DOMAIN must be a hostname without a scheme or path" ;;
  esac
  apt-get install -y caddy
  install -d -o root -g root -m 755 /etc/caddy
  printf '%s\n' "$AIOS_DOMAIN {" '    reverse_proxy 127.0.0.1:8787' '}' > /etc/caddy/Caddyfile
  systemctl enable --now caddy
  echo "Caddy is serving https://${AIOS_DOMAIN} and proxying to the private dashboard."
else
  echo "The dashboard binds to localhost. Use an SSH tunnel; set AIOS_DOMAIN on a fresh install for automatic HTTPS."
fi

run_step 13 "building the map"
sudo -u aios bash -lc "cd /opt/aios/app && /opt/aios/venv/bin/python scripts/bootstrap.py && /opt/aios/venv/bin/python scripts/install_business_os.py --root . && /opt/aios/venv/bin/python scripts/sync_runtime_skills.py && /opt/aios/venv/bin/python scripts/build_map.py && /opt/aios/venv/bin/python scripts/build_diagrams.py" || echo "Skill import or map build needs the installed skills and will be retried after setup."

run_step 14 "enabling services and schedules"
systemctl enable --now aios-dashboard aios-bridge
echo "Schedules are installed but disabled until the owner approves them on Day 7."

run_step 15 "complete"
if [ -n "${AIOS_DOMAIN:-}" ]; then
  echo "Dashboard: https://${AIOS_DOMAIN}"
else
  echo "Dashboard: http://127.0.0.1:8787 through an SSH tunnel"
fi
echo "Status: systemctl status aios-dashboard aios-bridge"
