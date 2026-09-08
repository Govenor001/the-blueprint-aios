#!/usr/bin/env bash
set -euo pipefail

STEP=0
fail() { echo "[${STEP}/15] failed: $*" >&2; exit 1; }
run_step() { STEP="$1"; shift; echo "[${STEP}/15] $*"; }

run_step 1 "checking platform and target"
[ "$(lsb_release -rs 2>/dev/null || true)" = "24.04" ] || fail "Ubuntu 24.04 is required"
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
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-venv git ffmpeg curl ca-certificates

run_step 3 "checking Node 22 and Claude Code prerequisites"
command -v node >/dev/null || fail "Node 22 is required; install it before running this script"
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

run_step 9 "Claude subscription authentication"
echo "Run as aios: sudo -u aios claude setup-token"
echo "Approve the link on your phone, paste the code, then verify: sudo -u aios claude -p 'say ok'"

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
echo "The dashboard binds to localhost. Use an SSH tunnel or add a reviewed HTTPS reverse proxy."

run_step 13 "building the map"
sudo -u aios bash -lc "cd /opt/aios/app && /opt/aios/venv/bin/python scripts/bootstrap.py && /opt/aios/venv/bin/python scripts/build_map.py" || echo "Map build needs the installed skills and will be retried after setup."

run_step 14 "enabling services and schedules"
systemctl enable --now aios-dashboard aios-bridge
systemctl enable --now aios-brief.timer aios-inbox.timer aios-newsletter.timer

run_step 15 "complete"
echo "Dashboard: http://127.0.0.1:8787 through an SSH tunnel"
echo "Status: systemctl status aios-dashboard aios-bridge"
