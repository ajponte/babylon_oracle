#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
BAO_ADDR="http://127.0.0.1:8200"
BAO_DATA_DIR="./bao-data"
BAO_CONFIG_FILE="./bao.hcl"
BAO_UNSEAL_KEY_FILE="./unseal.key"
BAO_ROOT_TOKEN_FILE="./root.token"
BAO_LOG_FILE="./bao.log"

# --- Functions ---

start_server() {
  if pgrep -f "bao server" > /dev/null; then
    echo "Bao server already running."
    return
  fi

  echo "Starting Bao server..."
  mkdir -p "$BAO_DATA_DIR"

  cat > "$BAO_CONFIG_FILE" <<EOF
storage "file" {
  path = "$BAO_DATA_DIR"
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = true
}

disable_mlock = true
ui = true

secret "kv-v2" {
    path = "secret"
}
EOF

  bao server -config="$BAO_CONFIG_FILE" > "$BAO_LOG_FILE" 2>&1 &
  BAO_PID=$!
  echo "Bao started with PID $BAO_PID"
  echo "Logs: $BAO_LOG_FILE"

  # Wait until it's responsive
  until curl -s "$BAO_ADDR/v1/sys/health" > /dev/null 2>&1; do
    sleep 1
  done
  echo "Server is responsive."
}

initialize_server() {
  if [[ -f "$BAO_UNSEAL_KEY_FILE" && -f "$BAO_ROOT_TOKEN_FILE" ]]; then
    echo "Already initialized."
    return
  fi

  echo "Initializing Bao via API..."

  INIT_JSON=$(curl --silent --request PUT \
    --data '{"secret_shares":1,"secret_threshold":1}' \
    "$BAO_ADDR/v1/sys/init")

  if echo "$INIT_JSON" | jq -e '.root_token' > /dev/null 2>&1; then
    UNSEAL_KEY=$(echo "$INIT_JSON" | jq -r '.keys[0]')
    ROOT_TOKEN=$(echo "$INIT_JSON" | jq -r '.root_token')
  else
    echo "Initialization failed. Response:"
    echo "$INIT_JSON"
    exit 1
  fi

  echo "$UNSEAL_KEY" > "$BAO_UNSEAL_KEY_FILE"
  echo "$ROOT_TOKEN" > "$BAO_ROOT_TOKEN_FILE"
  echo "Initialization complete. Keys saved."
}

unseal_server() {
  export BAO_ADDR="http://127.0.0.1:8200"   # <— force HTTP, not HTTPS

  SEALED=$(curl -s "$BAO_ADDR/v1/sys/health" | jq -r '.sealed')
  if [[ "$SEALED" == "false" ]]; then
    echo "Server already unsealed."
    return
  fi

  UNSEAL_KEY=$(cat "$BAO_UNSEAL_KEY_FILE")
  echo "Unsealing Bao..."
  bao operator unseal "$UNSEAL_KEY"
  echo "Unseal complete."
}


export_env() {
  ROOT_TOKEN=$(cat "$BAO_ROOT_TOKEN_FILE")
  echo "Exporting environment variables..."
  export BAO_ADDR="$BAO_ADDR"
  export BAO_TOKEN="$ROOT_TOKEN"

  echo
  echo "✅ Bao is ready."
  echo "Address: $BAO_ADDR"
  echo "Root Token: $BAO_TOKEN"
  echo
  echo "To use the CLI in this shell, run:"
  echo "export BAO_ADDR=$BAO_ADDR"
  echo "export BAO_TOKEN=$BAO_TOKEN"
}

# --- Main Flow ---
start_server
initialize_server
unseal_server

  echo "Enabling kv-v2 secrets engine..."
  export BAO_ADDR="$BAO_ADDR"
  export BAO_TOKEN=$(cat "$BAO_ROOT_TOKEN_FILE")
  bao secrets enable -path=secret kv-v2 || echo "Secrets engine already enabled."

export_env
