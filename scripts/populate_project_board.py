#!/usr/bin/env python3
"""
Populate the BaoPSU user Projects v2 board (https://github.com/users/BaoPSU/projects/1)
with the capstone task backlog, each as a draft card with an Owner, a Status, and a
Start date spread across the term (Jan -> May 31, 2026).

This talks to GitHub's GraphQL Projects v2 API using YOUR account. Nothing is sent
until you run it.

------------------------------------------------------------------------------
SETUP (one time)
------------------------------------------------------------------------------
You need a token with Projects write access:

  Option A - GitHub CLI (easiest):
      gh auth login
      gh auth refresh -s project,read:project      # add the project scopes
      # the script will pick the token up automatically via `gh auth token`

  Option B - Personal access token:
      Create a token at https://github.com/settings/tokens
        * classic token: check the  project  scope (and  repo  if you later link issues)
        * or fine-grained: give it  Projects: Read and write
      export GITHUB_TOKEN=ghp_xxx

No third-party packages needed (uses the Python standard library only).

------------------------------------------------------------------------------
RUN
------------------------------------------------------------------------------
      python3 scripts/populate_project_board.py            # create the cards
      python3 scripts/populate_project_board.py --dry-run  # print what it would do

Re-running is safe: cards whose title already exists are skipped.
"""
import os
import sys
import subprocess
import json
import urllib.request
import urllib.error

OWNER = "BaoPSU"          # the user who owns the project
PROJECT_NUMBER = 1        # github.com/users/BaoPSU/projects/1
DATE_FIELD_NAME = "Start date"
OWNER_FIELD_NAME = "Owner"
API = "https://api.github.com/graphql"
DRY = "--dry-run" in sys.argv

# ----------------------------------------------------------------------------
# Task backlog: (title, owner, status, date YYYY-MM-DD, body)
# Owners: Yaqoub (PLC+HMI), Fearghus (CAD/schematics), Bao (wiring+sizing),
#         Fox (capacitive-touch module), Team (shared).
# Status is matched loosely against the board's Status options.
# ----------------------------------------------------------------------------
TASKS = [
    # --- Planning / early term ---
    ("Finalize requirements & project scope", "Team", "Done", "2026-01-12",
     "Lock the must/should/may requirements and EE vs ME scope split."),
    ("VFD selection (decision matrix)", "Bao", "Done", "2026-01-20",
     "Compare VFD options on price/documentation/reliability; chose Huanyang HY02D211B-T."),
    ("Motor spec & sizing", "Bao", "Done", "2026-01-26",
     "Size the motor (3-5 HP, 70-90 RPM output). Bench/test motor: GE 5KE182BC205B."),

    # --- February ---
    ("PLC ladder logic v1", "Yaqoub", "Done", "2026-02-06",
     "First ladder: deadman permissive, run command, jam/unjam state machine."),
    ("PLC I/O point list & I/O map", "Bao", "In Progress", "2026-02-20",
     "Assign every X/Y and analog point; keep Point List.xlsx as the source of truth."),
    ("Bill of materials", "Team", "Done", "2026-02-20",
     "Procurement BOM for the electrical system."),
    ("VFD parameter programming", "Yaqoub", "Done", "2026-02-25",
     "Program PD002/052/054/123/124/125 and motor params PD141-144."),

    # --- March ---
    ("Safety circuit design (E-stop chain)", "Bao", "In Progress", "2026-03-05",
     "Hardwired E22B1 NC -> SD-N35 contactor coil; X4 monitor tap."),
    ("Over-torque / jam-detection signal chain", "Yaqoub", "In Progress", "2026-03-12",
     "VFD fault relay FA/FC -> PLC X5; unjam routine with RST pulse + 3-strike lockout."),
    ("HMI screen programming", "Yaqoub", "In Progress", "2026-03-20",
     "C-More EA1-T4CL screens: Ready/Running/Jam/Lockout/Fault, reset, status data."),
    ("CAD schematic: power distribution", "Fearghus", "In Progress", "2026-03-25",
     "AC in -> disconnect -> branch breakers -> VFD and 24 V PSU."),

    # --- April ---
    ("CAD schematics: safety + PLC/HMI wiring", "Fearghus", "Todo", "2026-04-05",
     "Safety-circuit schematic, PLC/HMI wiring diagram, panel layout."),
    ("Panel wiring & build", "Bao", "In Progress", "2026-04-15",
     "Land conductors, run the panel, ferrule control wiring."),
    ("Capacitive-touch (CTSI) module: program & build", "Fox", "In Progress", "2026-04-20",
     "Build the module; the ladder logic on X7 (touch -> stop) is already written."),
    ("Scale/configure motor-current monitor", "Yaqoub", "Todo", "2026-04-25",
     "VFD VO -> F2-08AD-1 CH1: set the VFD analog-out and PLC analog-in scaling (wired, not yet calibrated)."),

    # --- May ---
    ("CTSI module: integrate & test (wire to X7)", "Fox", "Todo", "2026-05-05",
     "Wire the on-hand CTSI module to X7 and validate the touch-trip stop."),
    ("Signal-chain validation tests", "Yaqoub", "Todo", "2026-05-10",
     "Jumper test, guaranteed-trip test, threshold tuning; confirm PLC reacts."),
    ("Resolve NFPA 79 neutral-switching deviation", "Bao", "Todo", "2026-05-12",
     "As-built switches the neutral leg; switch the hot leg per NEC/NFPA 79 (or justify + risk-assess)."),
    ("Select final production motor", "Bao", "Todo", "2026-05-15",
     "Production motor is TBD (3-5 HP); pick it and re-verify NEC 430 sizing."),
    ("Measure E-stop & two-hand response times", "Team", "Todo", "2026-05-18",
     "Scope the E-stop stop time and the two-hand simultaneous-release behavior."),
    ("Export wiring diagrams -> report Appendix C", "Fearghus", "Todo", "2026-05-20",
     "Export AutoCAD schematics as PDFs for Appendix C and a system block diagram."),
    ("ISO 13849-1 PL assessment / advisor sign-off", "Bao", "Todo", "2026-05-22",
     "Preliminary assessment is Cat B-1; confirm with advisor whether formal PL is in scope."),
    ("Load testing with plastic samples", "Team", "Todo", "2026-05-26",
     "Test under real shredding load once ME integration is ready."),
    ("Final report draft", "Team", "Todo", "2026-05-31",
     "Assemble the EE final report; owners write their sections."),
]

# Owner -> single-select color (GitHub palette)
OWNER_COLORS = {
    "Yaqoub": "BLUE", "Fearghus": "GREEN", "Bao": "PURPLE",
    "Fox": "ORANGE", "Team": "GRAY",
}


def get_token():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok.strip()
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception:
        sys.exit("No token: set GITHUB_TOKEN or run `gh auth login` "
                 "(and `gh auth refresh -s project`).")


TOKEN = get_token()


def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=payload, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "shredder-project-populator",
    })
    try:
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()}")
    if "errors" in data:
        sys.exit("GraphQL error: " + json.dumps(data["errors"], indent=2))
    return data["data"]


def load_project():
    q = """
    query($login:String!, $number:Int!){
      user(login:$login){ projectV2(number:$number){
        id title
        fields(first:50){ nodes{
          __typename
          ... on ProjectV2FieldCommon { id name dataType }
          ... on ProjectV2SingleSelectField { id name options{ id name } }
        }}
        items(first:100){ nodes{ id content{ ... on DraftIssue { title } } } }
      }}}"""
    p = gql(q, {"login": OWNER, "number": PROJECT_NUMBER})["user"]["projectV2"]
    if not p:
        sys.exit(f"Project #{PROJECT_NUMBER} not found for user {OWNER} "
                 "(is the token's owner the project owner?).")
    return p


def ensure_date_field(pid, fields):
    for f in fields:
        if f.get("name") == DATE_FIELD_NAME and f.get("dataType") == "DATE":
            return f["id"]
    if DRY:
        print(f"[dry-run] would create DATE field '{DATE_FIELD_NAME}'")
        return None
    m = """mutation($pid:ID!,$name:String!){
      createProjectV2Field(input:{projectId:$pid,dataType:DATE,name:$name}){
        projectV2Field{ ... on ProjectV2Field { id } } }}"""
    return gql(m, {"pid": pid, "name": DATE_FIELD_NAME})["createProjectV2Field"]["projectV2Field"]["id"]


def ensure_owner_field(pid, fields):
    for f in fields:
        if f.get("name") == OWNER_FIELD_NAME and "options" in f:
            return f["id"], {o["name"]: o["id"] for o in f["options"]}
    opts = [{"name": n, "color": c, "description": ""} for n, c in OWNER_COLORS.items()]
    if DRY:
        print(f"[dry-run] would create single-select '{OWNER_FIELD_NAME}' "
              f"with options {list(OWNER_COLORS)}")
        return None, {}
    m = """mutation($pid:ID!,$name:String!,$opts:[ProjectV2SingleSelectFieldOptionInput!]!){
      createProjectV2Field(input:{projectId:$pid,dataType:SINGLE_SELECT,name:$name,
        singleSelectOptions:$opts}){
        projectV2Field{ ... on ProjectV2SingleSelectField { id options{ id name } } } }}"""
    f = gql(m, {"pid": pid, "name": OWNER_FIELD_NAME, "opts": opts})
    sel = f["createProjectV2Field"]["projectV2Field"]
    return sel["id"], {o["name"]: o["id"] for o in sel["options"]}


def find_status_field(fields):
    for f in fields:
        if f.get("name") == "Status" and "options" in f:
            return f["id"], {o["name"].lower(): o["id"] for o in f["options"]}
    return None, {}


def add_draft(pid, title, body):
    m = """mutation($pid:ID!,$t:String!,$b:String!){
      addProjectV2DraftIssue(input:{projectId:$pid,title:$t,body:$b}){
        projectItem{ id } }}"""
    return gql(m, {"pid": pid, "t": title, "b": body})["addProjectV2DraftIssue"]["projectItem"]["id"]


def set_date(pid, item, field, date):
    m = """mutation($p:ID!,$i:ID!,$f:ID!,$d:Date!){
      updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,
        value:{date:$d}}){ projectV2Item{ id } }}"""
    gql(m, {"p": pid, "i": item, "f": field, "d": date})


def set_select(pid, item, field, option_id):
    m = """mutation($p:ID!,$i:ID!,$f:ID!,$o:String!){
      updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,
        value:{singleSelectOptionId:$o}}){ projectV2Item{ id } }}"""
    gql(m, {"p": pid, "i": item, "f": field, "o": option_id})


def match_status(status_map, wanted):
    w = wanted.lower()
    if w in status_map:
        return status_map[w]
    aliases = {"todo": ["to do", "backlog"], "in progress": ["in-progress", "doing"]}
    for a in aliases.get(w, []):
        if a in status_map:
            return status_map[a]
    return None


def main():
    proj = load_project()
    pid = proj["id"]
    fields = proj["fields"]["nodes"]
    existing = {n["content"]["title"] for n in proj["items"]["nodes"]
                if n.get("content") and n["content"].get("title")}
    print(f"Project: {proj['title']}  ({len(existing)} existing items)")

    date_fid = ensure_date_field(pid, fields)
    owner_fid, owner_opts = ensure_owner_field(pid, fields)
    status_fid, status_opts = find_status_field(fields)

    created = skipped = 0
    for title, owner, status, date, body in TASKS:
        if title in existing:
            skipped += 1
            continue
        if DRY:
            print(f"[dry-run] + {date}  [{owner:8}] {status:12} {title}")
            created += 1
            continue
        item = add_draft(pid, title, body + f"\n\nOwner: {owner}")
        if date_fid:
            set_date(pid, item, date_fid, date)
        if owner_fid and owner in owner_opts:
            set_select(pid, item, owner_fid, owner_opts[owner])
        if status_fid:
            oid = match_status(status_opts, status)
            if oid:
                set_select(pid, item, status_fid, oid)
        print(f"+ {date}  [{owner:8}] {status:12} {title}")
        created += 1

    print(f"\nDone. created={created} skipped(existing)={skipped}"
          + ("   (dry run, nothing written)" if DRY else ""))


if __name__ == "__main__":
    main()
