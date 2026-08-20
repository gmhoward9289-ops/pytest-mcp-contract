#!/usr/bin/env bash
# Read-only: does PyPI actually serve the version __init__.py claims?
#
# Job status is not the same fact — a green release.yml can still leave PyPI
# stale if OIDC was misconfigured once. This asks the registry, on a schedule
# and after each release.
#
# Channels for pytest-mcp-contract: git tag + PyPI only (no npm/tap/winget).
# release.yml does not attach GitHub Release assets; PyPI is the install path.
set -u

OWNER=gmhoward9289-ops
REPO=$OWNER/pytest-mcp-contract
DIST=pytest-mcp-contract
ROOT=$(cd "$(dirname "$0")/.." && pwd)

GRACE_MIN=${PUBLISH_DOCTOR_GRACE_MIN:-60}

VERSION=$(PYTHONPATH="$ROOT/src" python3 -c 'from mcp_contract import __version__; print(__version__)' 2>/dev/null)
if [ -z "$VERSION" ]; then
  echo "FATAL: could not read __version__ from src/mcp_contract/__init__.py" >&2
  exit 2
fi

fails=0
pendings=0
todos=0

say()  { printf '  %-8s %-10s %s\n' "$1" "$2" "$3"; }
pass() { say PASS "$1" "$2"; }
skip() { say "--" "$1" "$2"; }
todo() { say TODO "$1" "$2"; todos=$((todos + 1)); }
pend() { say PENDING "$1" "$2"; pendings=$((pendings + 1)); }
fail() { say FAIL "$1" "$2"; fails=$((fails + 1)); }

lagging() {
  if [ "$fresh" = 1 ]; then
    pend "$1" "$2 [$why_fresh]"
  else
    fail "$1" "$2"
  fi
}

echo "pytest-mcp-contract publish doctor -- version $VERSION (read-only)"
echo

published=$(gh release view "v$VERSION" --repo "$REPO" --json publishedAt \
              --jq '.publishedAt' 2>/dev/null)
if [ -n "${published:-}" ]; then
  age_min=$(python3 -c '
import datetime, sys
t = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%dT%H:%M:%SZ")
t = t.replace(tzinfo=datetime.timezone.utc)
print(int((datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() // 60))
' "$published" 2>/dev/null)
  : "${age_min:=99999}"
  if [ "$age_min" -lt "$GRACE_MIN" ]; then fresh=1; else fresh=0; fi
  why_fresh="release is ${age_min}m old, inside the ${GRACE_MIN}m window"
else
  fresh=1
  why_fresh="no v$VERSION GitHub release yet (optional; PyPI is the install channel)"
fi

tags=$(gh api "repos/$REPO/git/refs/tags" --jq '.[].ref' 2>/dev/null | sed 's#refs/tags/##')
latest_tag=$(printf '%s\n' "$tags" | grep -v '^$' | sed 's/^v//' | sort -V | tail -1)
if printf '%s\n' "$tags" | grep -qx "v$VERSION"; then
  pass "git tag" "v$VERSION is on the remote"
elif [ -z "${latest_tag:-}" ]; then
  todo "git tag" "no tags on $REPO yet"
elif [ "$(printf '%s\n%s\n' "$latest_tag" "$VERSION" | sort -V | tail -1)" = "$VERSION" ]; then
  pend "git tag" "newest tag is v$latest_tag, __init__ says $VERSION -- tag not cut yet"
else
  fail "git tag" "remote has v$latest_tag but __init__ says $VERSION"
fi

if [ -n "${published:-}" ]; then
  pass "gh release" "v$VERSION release exists (assets optional)"
else
  skip "gh release" "no v$VERSION release page -- OK; pip install $DIST uses PyPI"
fi

pypi=$(curl -sf "https://pypi.org/pypi/$DIST/json" 2>/dev/null)
if [ -z "$pypi" ]; then
  todo pypi "nothing on PyPI as $DIST -- pending publisher at https://pypi.org/manage/account/publishing/ (owner $OWNER, repo pytest-mcp-contract, workflow release.yml, environment pypi)"
else
  pypi_ver=$(printf '%s' "$pypi" | python3 -c 'import json,sys; print(json.load(sys.stdin)["info"]["version"])' 2>/dev/null)
  if [ "${pypi_ver:-}" = "$VERSION" ]; then
    names=$(printf '%s' "$pypi" | python3 -c '
import json, sys
print(" ".join(f["filename"] for f in json.load(sys.stdin)["urls"]))' 2>/dev/null)
    want_whl="pytest_mcp_contract-$VERSION-py3-none-any.whl"
    want_sdist="pytest_mcp_contract-$VERSION.tar.gz"
    case " $names " in
      *" $want_whl "*) ;;
      *) fail pypi "serves $pypi_ver but no $want_whl among: ${names:-<none>}" ;;
    esac
    case " $names " in
      *" $want_sdist "*) ;;
      *) fail pypi "serves $pypi_ver but no $want_sdist among: ${names:-<none>}" ;;
    esac
    pass pypi "pip install $DIST ($pypi_ver)"
  else
    lagging pypi "registry has ${pypi_ver:-<unparseable>}, want $VERSION -- rerun release.yml on tag v$VERSION"
  fi
fi

if [ -n "${GITHUB_ACTIONS:-}" ]; then
  skip secret "PyPI uses OIDC trusted publishing; no repo secrets to check"
else
  envs=$(gh api "repos/$REPO/environments/pypi" --jq '.name' 2>/dev/null)
  if [ "${envs:-}" = "pypi" ]; then
    pass secret "GitHub Environment pypi exists (OIDC)"
  else
    todo secret "create GitHub Environment named pypi on $REPO (Settings → Environments)"
  fi
fi

echo
printf 'pending %d  todo %d  fail %d\n' "$pendings" "$todos" "$fails"
if [ "$fails" -ne 0 ]; then
  echo
  echo "FAIL means PyPI disagrees with $VERSION and propagation is not the explanation."
  echo "Rerun the failed release job:"
  echo "  gh workflow run release.yml --repo $REPO --ref v$VERSION"
  exit 1
fi
if [ "$todos" -ne 0 ]; then
  echo "TODO items are one-time setup, not breakage."
fi
echo "PyPI matches $VERSION (or nothing is established yet)."
